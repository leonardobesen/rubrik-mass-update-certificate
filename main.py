import argparse
import os

import connection.connect as connect
import file_manager.write_to_file as write_to_csv
from configuration.configuration import get_report_dir
from controller import controller


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
    logger = write_to_csv.configure_logger(console=False)

    try:
        rsc_access_token = connect.open_session()

        if args.csv_path:
            csv_path = args.csv_path
        else:
            csv_path = os.path.join(get_report_dir(), 'hosts.csv')

        logger.info("Starting certificate update run using CSV: %s", csv_path)

        hosts, errors = controller.run_update_certificate(
            access_token=rsc_access_token,
            csv_path=csv_path,
            logger=logger,
        )

        if args.dry_run:
            logger.info("Dry run completed without making certificate updates.")
        else:
            try:
                report_path = write_to_csv.generate_report("updated_certificates", hosts, errors=errors)
                logger.info("Updated certificate report written to: %s", report_path)
            except Exception as exc:
                logger.warning("Unable to write report: %s", exc)
    finally:
        if 'rsc_access_token' in locals():
            connect.close_session(rsc_access_token)
        write_to_csv.close_logger(logger)
