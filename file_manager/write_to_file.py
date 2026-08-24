import csv
import os
from typing import Iterable, Optional, List, Tuple, Any
from datetime import datetime


def generate_report(name: str, hosts: Any, errors: Optional[List[Tuple[str, str]]] = None, out_dir: str | None = None) -> str:
    """Write a timestamped .log file with execution info and errors.

    - `hosts` should be an iterable of objects with `id` and `name` attributes.
    - `errors` is an optional list of `(host_id, message)` tuples.

    Returns the path to the generated log file.
    """
    # Normalize hosts to a list that we can iterate safely.
    if hosts is None:
        hosts_list = []
    elif isinstance(hosts, (str, bytes)):
        # Treat a string/bytes as a single host identifier rather than an iterable of chars
        hosts_list = [hosts]
    elif hasattr(hosts, "id") and hasattr(hosts, "name"):
        hosts_list = [hosts]
    else:
        try:
            hosts_list = list(hosts)
        except Exception:
            hosts_list = [hosts]

    if out_dir is None:
        out_dir = os.path.join(os.getcwd(), "reports")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, f"{name}.log")

    now = datetime.utcnow().isoformat() + "Z"

    with open(path, "w", newline="") as fh:
        fh.write(f"Execution time (UTC): {now}\n")
        fh.write("= Summary =\n")
        success_count = 0
        for h in hosts_list:
            hid = getattr(h, "id", None)
            hname = getattr(h, "name", None)
            if hid is None and isinstance(h, (str, bytes)):
                # If caller passed a hostname string, use it as the name
                hname = str(h)
            if hid is None:
                hid_str = "UNKNOWN"
            else:
                hid_str = str(hid)
            if hname is None:
                hname_str = "UNKNOWN"
            else:
                hname_str = str(hname)
            fh.write(f"SUCCESS: {datetime.utcnow().isoformat()} - id={hid_str} name={hname_str}\n")
            success_count += 1
        fh.write(f"Total successful updates: {success_count}\n")

        fh.write("\n= Errors =\n")
        if errors:
            for hid, msg in errors:
                fh.write(f"ERROR: {datetime.utcnow().isoformat()} - host_id={hid} - {msg}\n")
        else:
            fh.write("No errors reported.\n")

    return path
