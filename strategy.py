# strategy.py


'''
可以自己编写策略，这里仅仅默认提供两个策略
1.均线平缓和调头
2.经典双均线，可以修改参数

'''
from datetime import datetime, timedelta


def check_slope_alert(df, symbol, int_period, send_message_func, flat_threshold, last_alert_time):
    """
    检查斜率是否满足预警条件
    """
    period = f'{int_period}min'
    if df is not None and 'MA20_Slope' in df.columns:
        latest_slope = df['MA20_Slope'].iloc[-1]
        previous_slope = df['MA20_Slope'].iloc[-2] if len(df) > 1 else 0
        
        if abs(latest_slope) < flat_threshold:
            current_time = datetime.now()
            last_time = last_alert_time.get('slope_flat', None)
            if last_time is None or (current_time - last_time) > timedelta(minutes=45):
                message = f"[[MA20平缓][{period}]{symbol}]\n当前斜率为 {latest_slope}"
                print(message)
                send_message_func(message)
                last_alert_time['slope_flat'] = current_time
        
        if latest_slope * previous_slope < 0:
            current_time = datetime.now()
            last_time = last_alert_time.get('slope_reversal', None)
            if last_time is None or (current_time - last_time) > timedelta(minutes=45):
                message = f"[MA20调头][{period}][{symbol}]\n当前斜率为 {latest_slope}，前一个斜率为 {previous_slope}"
                print(message)
                send_message_func(message)
                last_alert_time['slope_reversal'] = current_time

def check_ma_cross(df, symbol, int_period, ma_short, ma_long, send_message_func):
    """
    检查两条均线是否构成金叉或死叉
    :param df: 包含均线数据的 DataFrame
    :param symbol: 期货合约代码
    :param int_period: 周期（如 5），用于通知，整数
    :param ma_short: 短期均线列名（如 'MA_20'）
    :param ma_long: 长期均线列名（如 'MA_60'）
    :param send_message_func: 发送消息的函数
    :param check_ma_arrangement: 控制是否发送金叉信息的标志（1 表示发送，其他值不发送）
    """
    period = f'{int_period}min'
    if df is not None and all(col in df.columns for col in [ma_short, ma_long]):
        ma_short_value = df[ma_short].iloc[-1]  # 短期均线最新值
        ma_long_value = df[ma_long].iloc[-1]    # 长期均线最新值
        
        # 获取前一个 K 线的均线值
        if len(df) > 1:
            prev_ma_short = df[ma_short].iloc[-2]
            prev_ma_long = df[ma_long].iloc[-2]
        else:
            prev_ma_short = ma_short_value
            prev_ma_long = ma_long_value
        
        # 判断是否构成金叉（短期均线上穿长期均线）
        if prev_ma_short < prev_ma_long and ma_short_value > ma_long_value:
            message = f"[金叉][{period}][{symbol}]\n当前{ma_short}={ma_short_value}，{ma_long}={ma_long_value}"
            print(message)
            send_message_func(message)
        
        # 判断是否构成死叉（短期均线下穿长期均线）
        if prev_ma_short > prev_ma_long and ma_short_value < ma_long_value:
            message = f"[死叉][{period}][{symbol}]\n当前{ma_short}={ma_short_value}，{ma_long}={ma_long_value}"
            print(message)
            send_message_func(message)
           
            