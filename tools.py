# tools.py
from datetime import datetime, time as dt_time

def is_trade_time(trade_morning_start, trade_morning_end, trade_afternoon_start, trade_afternoon_end, trade_night_start, trade_night_end):
    """
    判断当前时间是否为交易时间段
    """
    now = datetime.now()
    now_time = now.time()
    is_morning = trade_morning_start <= now_time <= trade_morning_end
    is_afternoon = trade_afternoon_start <= now_time <= trade_afternoon_end
    is_night = trade_night_start <= now_time <= trade_night_end
    return is_morning or is_afternoon or is_night


