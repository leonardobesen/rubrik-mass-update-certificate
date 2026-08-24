import random
from model.hosts import Host
from time import sleep
from tqdm import tqdm
from data.data_operation import create_linux_host_from_data
from file_manager.read_csv import read_hostnames
from graphql.service import get_host_ids, update_certificate


def _get_host_ids_from_csv(csv_path: str, access_token: str) -> list[str]:
    """Read hostnames from CSV and resolve to host IDs via `graphql.service`.
    Returns a list of host ids (may contain duplicates).
    """
    hosts_ids: list[str] = []
    hostnames = read_hostnames(csv_path)

    for hostname in hostnames:
        try:
            ids = get_host_ids(access_token, hostname)
        except Exception as e:
            print(f"ERROR: Unable to fetch host id for {hostname}: {e}")
            continue
        hosts_ids.extend(ids)

    return hosts_ids


def run_update_certificate(access_token: str, csv_path: str) -> tuple[list[Host], list[tuple[str, str]]]:
    """Run update certificate for hosts resolved from CSV.

    Returns a tuple of (successful_hosts, errors) where errors is a list
    of tuples (host_id, error_message).
    """
    host_executed: list[Host] = []
    errors: list[tuple[str, str]] = []
    hosts = _get_host_ids_from_csv(csv_path, access_token)

    # Ensure we don't process duplicate host IDs (preserve order)
    seen: set[str] = set()
    unique_hosts: list[str] = []
    for h in hosts:
        if h and h not in seen:
            seen.add(h)
            unique_hosts.append(h)
    hosts = unique_hosts

    for host in tqdm(hosts, desc="Running Update Certificate on Hosts"):
        try:
            response = update_certificate(access_token, host)
            host_dict = response.get("data", {}).get("bulkUpdateHost", {}).get(
                "output", {}).get("items")[0].get("hostSummary", {})
        except Exception as e:
            msg = str(e)
            print(f"ERROR: Unable to run command for host ID {host}: {msg}")
            errors.append((host, msg))
            continue

        if not host_dict:
            msg = "No host summary returned"
            print(f"ERROR: {msg} for host ID {host}")
            errors.append((host, msg))
            continue

        host_obj = create_linux_host_from_data(host_dict)
        if host_obj:
            host_executed.append(host_obj)
            print(f"INFO: Updated Certificate on host {host_obj.name} (ID: {host_obj.id})")
        else:
            msg = "Failed to create Host object from response"
            print(f"ERROR: {msg} for host ID {host}")
            errors.append((host, msg))

        # Because sometimes RSC feels like you are spamming it ¯\_(ツ)_/¯
        sleep(random.uniform(1.0, 3.0))

    return host_executed, errors
