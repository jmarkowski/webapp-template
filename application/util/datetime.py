from datetime import datetime


def now_str(format='%Y-%m-%d, %H:%M:%S'):
    return datetime.now().strftime(format)
