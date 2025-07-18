import csv
import random
from model.hosts import Host
from time import sleep
from graphql import queries
from tqdm import tqdm
from data.data_operation import create_linux_host_from_data
from connection.wrapper import request


def _get_host_ids_from_csv(csv_path: str) -> list[str]:
    hosts_ids = []

    with open(csv_path, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            hosts_ids.append(row[0])

    return hosts_ids


def run_update_certificate(access_token: str, csv_path: str) -> list[Host]:
    host_executed = []
    hosts = _get_host_ids_from_csv(csv_path)

    for host in tqdm(hosts, desc="Running Update Certificate on Hosts"):
        query, variables = queries.update_certificate_for_host(host)

        try:
            response = request(access_token, query, variables)
        except:
            print("ERROR: Unable to run command for host ID {host}")
            continue

        host_dict = response.get("data", {}).get("bulkUpdateHost", {}).get(
            "output", {}).get("items")[0].get("hostSummary", {})

        if host_dict:
            host_obj = create_linux_host_from_data(host_dict)
            host_executed.append(host_obj)
            print(
                f"INFO: Updated Certificateon host {host_obj.name} (ID: {host_obj.id})")

        # Because sometimes RSC feels like you are spamming it ¯\_(ツ)_/¯
        sleep(random.uniform(1.0, 3.0))

    return host_executed
