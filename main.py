import connection.connect as connect
import file_manager.write_to_file as write_to_csv
from controller import controller
from configuration.configuration import get_report_dir
import os


if __name__ == '__main__':
    # Establish connection with Rubrik RSC
    rsc_access_token = connect.open_session()

    csv_path = os.path.join(get_report_dir(), 'host_ids.csv')

    hosts = controller.run_update_certificate(
        access_token=rsc_access_token,
        csv_path=csv_path
    )

    write_to_csv.generate_report("updated_certificates", hosts)

    # Close session
    connect.close_session(rsc_access_token)
