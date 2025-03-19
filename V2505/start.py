import sys
import os
import threading

# 获取当前脚本所在的目录
current_dir = os.path.dirname(os.path.abspath(__file__))

# 将当前目录添加到 sys.path（如果尚未添加）
if current_dir not in sys.path:
    sys.path.append(current_dir)

# 现在可以直接导入 config.py 中的 Config 类
from config import Config

# 获取主文件夹的绝对路径
main_folder_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# 将主文件夹路径添加到 sys.path（如果尚未添加）
if main_folder_path not in sys.path:
    sys.path.append(main_folder_path)

# 导入 Main 类
from main import Main
from notifier import send_wechat_message

# 设置 config
config = Config()

# 定义一个函数，用于在线程中运行 main.run() 并捕获异常
def run_main(config, period):
    try:
        main = Main(config, period)
        main.run()
        return True  # 表示成功
    except Exception as e:
        error_mes=f"{config.symbol}Error in thread with period {period}: {e}"
        print(error_mes)
        send_wechat_message(error_mes,config.bot_url)
        return False  # 表示失败

# 创建线程列表和结果列表
threads = []
results = []

# 遍历 config.periods，为每个 period 创建一个线程
for p in config.periods:
    thread = threading.Thread(target=lambda p=p: results.append(run_main(config, p)))
    threads.append(thread)
    thread.start()


# 检查所有线程是否成功
if all(results):
    sec_mes=f"{config.symbol}全部启动成功"
    print(sec_mes)
    send_wechat_message(sec_mes,config.bot_url)
else:
    print("Some threads encountered errors.")