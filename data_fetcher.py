# data_fetcher.py
import akshare as ak

def get_futures_data(symbol, period):
    """
    获取期货period分钟数据
    """
    try:
        df = ak.futures_zh_minute_sina(symbol=symbol, period=period)
        if df.empty:
            print("获取的数据为空，请检查期货品种或数据源。")
            return None
        required_columns = ['datetime', 'open', 'high', 'low', 'close', 'volume']
        if not all(col in df.columns for col in required_columns):
            print(f"数据列不匹配，获取的数据列名为: {df.columns}")
            return None
        return df
    except Exception as e:
        print(f"获取数据时出错: {e}")
        return None