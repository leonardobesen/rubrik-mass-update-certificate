import connection.connect as connect
import file_manager.write_to_file as write_to_csv
from controller import controller
from configuration.configuration import get_report_dir
import os
import argparse


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run certificate update for hosts listed in a CSV file.")
    parser.add_argument(
        "-c",
        "--csv",
        dest="csv_path",
        help="Path to the CSV file containing hostnames. If omitted, uses reports/hosts.csv",
        default=None,
    )
    parser.add_argument(
        "--dry-run",
        dest="dry_run",
        action="store_true",
        help="Don't perform updates; only resolve host ids and print actions.",
    )
    return parser.parse_args()


if __name__ == '__main__':
    args = _parse_args()

    # Establish connection with Rubrik RSC
    rsc_access_token = connect.open_session()

    if args.csv_path:
        csv_path = args.csv_path
    else:
        csv_path = os.path.join(get_report_dir(), 'hosts.csv')

    hosts, errors = controller.run_update_certificate(
        access_token=rsc_access_token,
        csv_path=csv_path
    )

    if not args.dry_run:
        try:
            write_to_csv.generate_report("updated_certificates", hosts, errors=errors)
        except Exception as e:
            print(f"WARNING: Unable to write report: {e}")

    # Close session
    connect.close_session(rsc_access_token)
