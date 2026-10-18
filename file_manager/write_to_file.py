import logging
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable, List, Optional, Tuple


def configure_logger(log_path: str | None = None, console: bool = False, level: int = logging.INFO) -> logging.Logger:
    """Create a reusable logger that writes to a file and optionally stderr.

    Console output is disabled by default so tqdm can render a clean progress bar
    without mixing log lines and redraws.
    """
    logger = logging.getLogger("rubrik_mass_update")
    logger.setLevel(level)
    logger.propagate = False

    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.close()

    if log_path is None:
        reports_dir = Path.cwd() / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        log_path = str(reports_dir / "rubrik_mass_update.log")

    log_file = Path(log_path)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")

    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    if console:
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger


def close_logger(logger: logging.Logger | None = None) -> None:
    """Close all handlers for the configured logger."""
    logger = logger or logging.getLogger("rubrik_mass_update")
    for handler in list(logger.handlers):
        logger.removeHandler(handler)
        handler.flush()
        handler.close()


def _normalize_hosts(hosts: Any) -> list[Any]:
    if hosts is None:
        return []
    if isinstance(hosts, (str, bytes)):
        return [hosts]
    if hasattr(hosts, "id") and hasattr(hosts, "name"):
        return [hosts]
    try:
        return list(hosts)
    except TypeError:
        return [hosts]


def generate_report(name: str, hosts: Any, errors: Optional[List[Tuple[str, str]]] = None, out_dir: str | None = None) -> str:
    """Write a timestamped log file with execution info and errors.

    - `hosts` should be an iterable of objects with `id` and `name` attributes.
    - `errors` is an optional list of `(host_id, message)` tuples.

    Returns the path to the generated log file.
    """
    hosts_list = _normalize_hosts(hosts)

    report_dir = Path(out_dir) if out_dir is not None else Path.cwd() / "reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    path = report_dir / f"{name}.log"

    now = datetime.now(timezone.utc).isoformat()

    with path.open("w", encoding="utf-8", newline="") as fh:
        fh.write(f"Execution time (UTC): {now}\n")
        fh.write("= Summary =\n")
        success_count = 0
        for h in hosts_list:
            hid = getattr(h, "id", None)
            hname = getattr(h, "name", None)
            if hid is None and isinstance(h, (str, bytes)):
                hname = str(h)
            hid_str = str(hid) if hid is not None else "UNKNOWN"
            hname_str = str(hname) if hname is not None else "UNKNOWN"
            fh.write(f"SUCCESS: {datetime.now(timezone.utc).isoformat()} - id={hid_str} name={hname_str}\n")
            success_count += 1
        fh.write(f"Total successful updates: {success_count}\n")

        fh.write("\n= Errors =\n")
        if errors:
            for hid, msg in errors:
                fh.write(f"ERROR: {datetime.now(timezone.utc).isoformat()} - host_id={hid} - {msg}\n")
        else:
            fh.write("No errors reported.\n")

    return str(path)
