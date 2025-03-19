'''

ALTUR_Futures
阿图尔未来
作者：43Cas


'''



import time
from datetime import datetime
from data_fetcher import get_futures_data
from ma_calculator import calculate_ma, calculate_ma20_slope
from strategy import check_ma_cross,  check_slope_alert
from data_saver import save_data
from notifier import send_wechat_message
from tools import is_trade_time
import os



class Main:
    def __init__(self, config, period):
        self.config = config  # 配置对象
        self.symbol = self.config.symbol  # 期货合约代码
        self.period = period  # self.period为整数,比如5min
        self.last_alert_time = {}  # 用于记录上一次通知的时间

    

    def run(self):
        while True:
            now = datetime.now()
            print(f'{now.strftime("%Y-%m-%d %H:%M:%S")} 开始检查交易时间...')

            # 检查是否为交易时间
            if not self.is_trade_time():
                print("当前时间为非交易时间段，程序暂停运行。")
                time.sleep(60 * self.period)
                continue

            # 获取数据
            df = get_futures_data(self.symbol, self.period)
            if df is not None:
                # 计算均线和斜率
                df = self.calculate_indicators(df)

                if(self.period == 5):
                    self.strategy_5min(df)
                elif(self.period == 15):
                    self.strategy_15min(df)
                elif(self.period == 30 or self.period == 60):
                    self.strategy_30min_60min(df)

             

                # 保存数据
                file_name = f'{self.symbol}_{self.period}min.csv'  # 动态生成文件名
                file_path = os.path.join(self.config.file_path, file_name)  # 动态生成文件路径
                save_data(df, file_path)

            # 休眠
            time.sleep(60 * self.period)
        



    def strategy_5min(self,df):
        threshold_5min = 1
        self.check_ma_cross(df,'MA_20','MA_60')
        self.check_ma_cross(df,'MA_30','MA_60')
        

    def strategy_15min(self,df):
        threshold_15min = 2
        self.check_ma_cross(df,'MA_20','MA_30')
        self.check_ma_cross(df,'MA_20','MA_60')
        self.check_ma_cross(df,'MA_30','MA_60')
        
    def strategy_30min_60min(self,df):
        threshold_30min = 3
        self.check_ma_cross(df,'MA_20','MA_30')
        self.check_ma_cross(df,'MA_20','MA_60')
        self.check_ma_cross(df,'MA_30','MA_60')
        



    def is_trade_time(self):
        """判断当前是否为交易时间"""
        return is_trade_time(
            self.config.trade_morning_start, self.config.trade_morning_end,
            self.config.trade_afternoon_start, self.config.trade_afternoon_end,
            self.config.trade_night_start, self.config.trade_night_end
        )
    


    def calculate_indicators(self, df):
        """计算均线和斜率"""
        df = calculate_ma(df, self.config.ma_periods)
        df = calculate_ma20_slope(df)
        return df
    
    def check_slope_alert(self, df):
        # 检查斜率预警
        check_slope_alert(
            df, self.symbol, self.period,
            lambda msg: send_wechat_message(msg, self.config.bot_url),
            self.config.ma_flat_threshold, self.last_alert_time
        )

    def check_ma_cross(self, df,short_period,long_period):
        # 检查均线交叉
        check_ma_cross(
            df, self.symbol, self.period,short_period, long_period,
            lambda msg: send_wechat_message(msg, self.config.bot_url)
            
        )


        