import logging
import random
from time import sleep

from tqdm import tqdm

from data.data_operation import create_linux_host_from_data
from file_manager.read_csv import read_hostnames
from file_manager.write_to_file import configure_logger
from graphql.service import get_host_ids, update_certificate
from model.hosts import Host


def _get_host_ids_from_csv(csv_path: str, access_token: str, logger: logging.Logger | None = None) -> list[str]:
    """Read hostnames from CSV and resolve to host IDs via `graphql.service`.
    Returns a list of host ids (may contain duplicates).
    """
    logger = logger or configure_logger()
    hosts_ids: list[str] = []
    hostnames = read_hostnames(csv_path)

    for hostname in hostnames:
        try:
            ids = get_host_ids(access_token, hostname)
        except Exception as exc:
            logger.exception("Unable to fetch host id for %s", hostname)
            continue
        hosts_ids.extend(ids)

    logger.info("Resolved %s host IDs from %s hostnames.", len(hosts_ids), len(hostnames))
    return hosts_ids


def run_update_certificate(
    access_token: str,
    csv_path: str,
    logger: logging.Logger | None = None,
) -> tuple[list[Host], list[tuple[str, str]]]:
    """Run update certificate for hosts resolved from CSV.

    Returns a tuple of (successful_hosts, errors) where errors is a list
    of tuples (host_id, error_message).
    """
    logger = logger or configure_logger()
    host_executed: list[Host] = []
    errors: list[tuple[str, str]] = []
    hosts = _get_host_ids_from_csv(csv_path, access_token, logger=logger)

    seen: set[str] = set()
    unique_hosts: list[str] = []
    for h in hosts:
        if h and h not in seen:
            seen.add(h)
            unique_hosts.append(h)
    hosts = unique_hosts

    logger.info("Processing %s unique host IDs.", len(hosts))

    for host in tqdm(
        hosts,
        desc="Running Update Certificate on Hosts",
        unit="host",
        leave=False,
        dynamic_ncols=True,
    ):
        try:
            response = update_certificate(access_token, host)
            host_dict = response.get("data", {}).get("bulkUpdateHost", {}).get("output", {}).get("items", [])[0].get("hostSummary", {})
        except Exception as exc:
            msg = str(exc)
            logger.exception("Unable to run command for host ID %s", host)
            errors.append((host, msg))
            continue

        if not host_dict:
            msg = "No host summary returned"
            logger.error("%s for host ID %s", msg, host)
            errors.append((host, msg))
            continue

        host_obj = create_linux_host_from_data(host_dict)
        if host_obj:
            host_executed.append(host_obj)
            logger.info("Updated Certificate on host %s (ID: %s)", host_obj.name, host_obj.id)
        else:
            msg = "Failed to create Host object from response"
            logger.error("%s for host ID %s", msg, host)
            errors.append((host, msg))

        sleep(random.uniform(1.0, 3.0))

    logger.info("Finished certificate update run: %s successful hosts, %s errors.", len(host_executed), len(errors))
    return host_executed, errors
