from datetime import datetime, timedelta
from dateutil import parser

DELTA_6MONTHS = timedelta(weeks=4 * 6)


def yesterday() -> str:
    yesterday = now() - timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    return date_iso(yesterday)


def now():
    return datetime.utcnow()


def date_parsed(date: str, raw=False):
    date_dt = parser.parse(date)
    return date_dt if raw else date_iso(date_dt)


def date_iso(date: datetime) -> str:
    return (
        date.astimezone().replace(tzinfo=None).isoformat(timespec="milliseconds") + "Z"
    )
