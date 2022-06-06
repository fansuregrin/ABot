import time
import datetime as dt
import pytz


def format_timestamp(timestamp):
    local_time = time.localtime(timestamp)
    fmt_time = time.strftime('%Y-%m-%d %H:%M:%S', local_time)
    return fmt_time

def gen_date(timezone = 'Asia/Shanghai'):
    tz = pytz.timezone(timezone)
    date_ = dt.datetime.now(tz).isoformat().split('T')[0]
    return date_