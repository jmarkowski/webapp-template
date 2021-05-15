from datetime import datetime
from datetime import timezone


def now_str(fmt='%Y-%m-%d, %H:%M:%S'):
    return datetime.now().strftime(fmt)


def now_tz_utc():
    """Return an aware datetime object with the UTC as the timezone."""
    return datetime.now(timezone.utc)
