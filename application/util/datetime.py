from datetime import datetime
from datetime import timezone


def now_str(format='%Y-%m-%d, %H:%M:%S'):
    return datetime.now().strftime(format)


def now_tz_utc():
    """Return an aware datetime object with the UTC as the timezone."""
    return datetime.now(timezone.utc)
