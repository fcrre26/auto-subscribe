import requests
import re

# 1. 获取最新token
def fetch_latest_token():
    url = "https://github.com/wzdnzd/aggregator/issues/91"
    resp = requests.get(url)
    match = re.search(r'[a-z0-9]{15,}', resp.text)
    return match.group(0) if match else None

# 2. 获取订阅内容
def fetch_subscribe(token):
    url = f"https://ohayoo-pm.hf.space/api/v1/subscribe?token={token}&target=clash&list=true"
    resp = requests.get(url)
    return resp.text

if __name__ == "__main__":
    token = fetch_latest_token()
    if not token:
        print("No valid token found.")
        exit(1)
    content = fetch_subscribe(token)
    # 3. 保存为本地文件（比如 clash.yaml）
    with open("clash.yaml", "w", encoding="utf-8") as f:
        f.write(content)
    print("Subscribe updated.")
