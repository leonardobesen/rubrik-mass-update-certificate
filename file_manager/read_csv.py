import csv
from typing import List


def read_hostnames(csv_path: str) -> List[str]:
    """Read hostnames from a CSV file (first column). Skips empty rows and common headers."""
    hostnames: List[str] = []
    with open(csv_path, "r", newline="") as fh:
        reader = csv.reader(fh)
        for row in reader:
            if not row:
                continue
            name = row[0].strip()
            if not name:
                continue
            if name.lower() in ("hostname", "host", "name"):
                continue
            hostnames.append(name)
    return hostnames
