from typing import Optional
from model.hosts import Host


def create_linux_host_from_data(data: dict) -> Optional[Host]:
    try:
        return Host(
            id=data["id"],
            name=data["name"]
        )
    except Exception as e:
        print("Error processing Host item: ", e)
        return None

