import undetected_chromedriver as uc
import time
from selenium.webdriver.chrome.options import Options
import os
from fake_useragent import UserAgent

ua = UserAgent()
while True:
    ua_random = ua.random
    if any(x in ua_random for x in ["Windows", "Macintosh", "Linux"]):
        print(ua_random)
    time.sleep(1)

# --- 2. Tạo Options ---
chrome_options = Options()

# cấu hình profile
name_folder = 'youtube1'
user_data_dir = os.path.join(os.getcwd(), 'youtubes', name_folder)
user_data_dir_abspath = os.path.abspath(user_data_dir) 
chrome_options.add_argument(f"--user-data-dir={user_data_dir_abspath}")
chrome_options.add_argument("--profile-directory=Default") 

# cấu hình proxy
proxy = "156.230.235.168:8800"
chrome_options.add_argument(f"--proxy-server={proxy}")

# fake useragent
ua = UserAgent()
chrome_options.add_argument(f"--user-agent={ua.random}") 

chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

browser = uc.Chrome(options=chrome_options)
browser.get("https://youtube.com/")

print(browser.title)
time.sleep(10000)
browser.quit()
