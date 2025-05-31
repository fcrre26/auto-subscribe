import requests
import re

# 1. 获取最新token
def fetch_latest_token():
    url = "https://github.com/wzdnzd/aggregator/issues/91"
    resp = requests.get(url)
    # 打印整个页面内容 (方便确认获取到的页面是否正确)
    print("--- GitHub Page Full Content ---")
    print(resp.text)
    print("--- End of GitHub Page Full Content ---")

    # 尝试使用更宽松的正则表达式查找 "统一为" 后面的至少15个字母数字串
    # .*? 匹配零个或多个任意字符 (非贪婪)
    # ([a-z0-9]{15,}) 捕获至少15个小写字母或数字
    # 这个正则表达式尝试在获取到的页面文本中查找 "统一为" 后面跟着的看起来像 token 的字符串
    match = re.search(r'统一为.*?([a-z0-9]{15,})', resp.text)

    # 如果找到匹配项，则提取捕获组 (即token)
    extracted_token = match.group(1) if match else None

    # 新增：打印脚本提取到的 token
    print(f"--- Extracted Token: {extracted_token} ---")

    return extracted_token

# 2. 获取订阅内容
# 修改函数，接受一个 list_param 参数来控制 list 的值
def fetch_subscribe(token, list_param):
    # 根据 list_param 构建 URL
    url = f"https://ohayoo-pm.hf.space/api/v1/subscribe?token={token}&target=clash&list={list_param}"
    resp = requests.get(url)
    # 也可以在这里添加打印状态码和响应内容的语句，以便进一步排查
    # print(f"--- Subscribe API Status Code: {resp.status_code} ---")
    # print("--- Subscribe API Response Content (Partial) ---")
    # print(resp.text[:500]) # 打印前500字符
    # print("--- End of Subscribe API Response Content ---")
    return resp.text

if __name__ == "__main__":
    token = fetch_latest_token()
    if not token:
        print("No valid token found.")
        exit(1)

    # 获取 list=true 的内容并保存到 aggregator-true.yaml
    print("\nFetching subscribe content with list=true...")
    content_true = fetch_subscribe(token, "true")
    with open("aggregatortrue.yaml", "w", encoding="utf-8") as f:
        f.write(content_true)
    print("Subscribe with list=true updated in aggregatortrue.yaml.")

    # 获取 list=false 的内容并保存到 aggregator-false.yaml
    print("\nFetching subscribe content with list=false...")
    content_false = fetch_subscribe(token, "false")
    with open("aggregatorfalse.yaml", "w", encoding="utf-8") as f:
        f.write(content_false)
    print("Subscribe with list=false updated in aggregatorfalse.yaml.")
