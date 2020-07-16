from datetime import datetime


def now(format='%Y-%m-%d, %H:%M:%S'):
    return datetime.now().strftime(format)
