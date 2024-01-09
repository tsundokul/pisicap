from datetime import datetime, timedelta


def yesterday():
    today = datetime.utcnow()
    yesterday = today - timedelta(days=1)
    yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)
    return __date_iso(yesterday)


def __date_iso(date):
    return (
        date.astimezone().replace(tzinfo=None).isoformat(timespec="milliseconds") + "Z"
    )
