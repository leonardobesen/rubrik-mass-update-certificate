import pandas as pd
import os
from datetime import datetime
from configuration.configuration import get_report_dir
from model.hosts import Host


def _create_empty_file(report_name: str) -> str:
    # Get current datetime formatted
    now = datetime.now().strftime("%d-%m-%Y_%H_%M_%S")
    # Filename for your reports
    file_name = f'{report_name}_{now}.csv'
    report_path = os.path.join(get_report_dir(), file_name)

    return report_path


def generate_report(report_name: str, hosts: list[Host]) -> str:
    REPORT_FILE = _create_empty_file(report_name)

    # Directly write CSV data
    write_linux_host_data(REPORT_FILE, hosts)

    return REPORT_FILE


def write_linux_host_data(csv_path: str, linuxhosts: list[Host]) -> None:
    df = pd.DataFrame([{
        'Id': host.id,
        'Hostname': host.name
    } for host in linuxhosts])

    df.to_csv(csv_path, index=False)
