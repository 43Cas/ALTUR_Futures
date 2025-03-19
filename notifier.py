# notifier.py
import requests
import json

def send_wechat_message(content, webhook_url):
    """
    发送文本消息到企业微信群
    """
    headers = {"Content-Type": "application/json"}
    data = {
        "msgtype": "text",
        "text": {
            "content": content,
            "mentioned_mobile_list": ["your_number"]
        }
    }
    response = requests.post(webhook_url, headers=headers, data=json.dumps(data))
    print("发送结果:", response.json())