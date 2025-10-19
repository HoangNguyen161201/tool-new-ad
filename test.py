import requests

proxy = "156.241.255.216:8800"
proxies = {
    "http": f"http://{proxy}",
    "https": f"http://{proxy}"
}

try:
    response = requests.get("https://api.myip.com", proxies=proxies, timeout=10)
    if response.status_code == 200:
        print("✅ Proxy hoạt động!")
        print("IP qua proxy:", response.json())
    else:
        print("⚠️ Proxy phản hồi lỗi:", response.status_code)
except requests.exceptions.RequestException as e:
    print("❌ Proxy không hoạt động:", e)