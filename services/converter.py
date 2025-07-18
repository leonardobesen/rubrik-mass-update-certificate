from datetime import datetime, timedelta
from typing import Optional
from configuration.configuration import get_timezone_info
import pytz


def iso_time_str_to_date(iso_str: Optional[str], should_fix_timezone=True) -> Optional[datetime]:
    timezone = get_timezone_info()

    if not iso_str:
        return None

    try:
        date_obj = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
        if should_fix_timezone:
            date_obj = date_obj.astimezone(pytz.timezone(timezone))
        return date_obj.replace(tzinfo=None)
    except ValueError:
        print(f"Invalid ISO8601 format provided")
        return None


def bytes_to_tb(bytes_size: int) -> float:
    return round(bytes_size/(1000**4), 2)


def seconds_to_timedelta(long_value: Optional[int]) -> Optional[timedelta]:
    if not long_value:
        return None

    try:
        time_delta = timedelta(seconds=long_value)
    except:
        return None

    return time_delta
