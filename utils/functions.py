from datetime import datetime, timedelta
from dateutil import parser


def yesterday():
    today = datetime.utcnow()
    yesterday = today - timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    return __date_iso(yesterday)


def date_parsed(date: str):
    date_dt = parser.parse(date)
    return __date_iso(date_dt)


def __date_iso(date: datetime):
    return (
        date.astimezone().replace(tzinfo=None).isoformat(timespec="milliseconds") + "Z"
    )
