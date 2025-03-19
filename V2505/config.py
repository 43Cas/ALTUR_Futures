import os
from datetime import time as dt_time

# 获取当前文件夹的绝对路径
current_dir = os.path.dirname(os.path.abspath(__file__))

# 定义 data 文件夹的绝对路径
data_dir = os.path.join(current_dir, 'data')

class Config:
    symbol = 'V2505'  # 期货合约代码
    periods = [5,15,30,60]  # K线周期
    ma_periods = [20, 30, 60]  # MA_20,MA_30,MA_60
    
    ma_flat_threshold = 1.0  # 均线平缓阈值
    trade_morning_start = dt_time(8, 45)  # 上午交易开始时间
    trade_morning_end = dt_time(11, 45)  # 上午交易结束时间
    trade_afternoon_start = dt_time(13, 15)  # 下午交易开始时间
    trade_afternoon_end = dt_time(18, 15)  # 下午交易结束时间
    trade_night_start = dt_time(20, 55)  # 夜盘交易开始时间
    trade_night_end = dt_time(23, 15)  # 夜盘交易结束时间
    file_path = data_dir
    bot_url = "yourkey"  # 企业微信机器人 URL