# data_saver.py
import pandas as pd

def save_data(df, file_path):
    """
    保存数据到本地
    """
    if df is not None:
        try:
            existing_df = pd.read_csv(file_path)
            updated_df = pd.concat([existing_df, df], ignore_index=True)
            updated_df.drop_duplicates(subset=['datetime'], keep='last', inplace=True)
            updated_df.to_csv(file_path, index=False)
        except FileNotFoundError:
            df.to_csv(file_path, index=False)
        print(f"数据已保存到 {file_path}")
    else:
        print("数据为空，未保存。")