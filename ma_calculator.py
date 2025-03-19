# ma_calculator.py
import pandas as pd

def calculate_ma(df, ma_periods):
    """
    计算均线
    """
    if df is not None:
        for period in ma_periods:
            df[f'MA_{period}'] = df['close'].rolling(window=period, min_periods=1).mean().round(2)
    return df

def calculate_ma20_slope(df):
    """
    计算MA20的斜率
    """
    if df is not None and 'MA_20' in df.columns:
        df['MA20_Slope'] = df['MA_20'].diff().round(2)
    return df