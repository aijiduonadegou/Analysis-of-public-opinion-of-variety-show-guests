import json
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import pandas as pd
import os
import datetime

# 设置Edge选项
edge_options = Options()
# 如果需要无头模式，取消下面的注释
# edge_options.add_argument("--headless")
edge_options.add_argument("--disable-gpu")
edge_options.add_argument("--no-sandbox")
edge_options.add_argument("--disable-dev-shm-usage")

# 创建Service对象，指定路径（如果不在系统PATH中）
service_path = r'C:\Users\Administrator\AppData\Local\Microsoft\WindowsApps\msedgedriver.exe'  # 替换为你的msedgedriver路径
if not os.path.isfile(service_path):
    raise FileNotFoundError(f"The path is not a valid file: {service_path}")

service = Service(service_path)

# 启动Edge浏览器
driver = webdriver.Edge(service=service, options=edge_options)

# 设置User-Agent
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.48"
driver.execute_cdp_cmd('Network.setUserAgentOverride', {"userAgent": user_agent})

def convert_expiry_to_timestamp(expiry_str):
    """将ISO 8601格式的expiry时间转换为时间戳"""
    if isinstance(expiry_str, int):
        return expiry_str  # 如果已经是时间戳，直接返回
    dt = datetime.datetime.strptime(expiry_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    timestamp = int(dt.timestamp())
    return timestamp

def add_cookies(cookies_file, driver):
    """加载并添加Cookies"""
    with open(cookies_file, 'r') as f:
        cookies = json.load(f)
    
    for cookie in cookies:
        if "expiry" in cookie:
            cookie["expiry"] = convert_expiry_to_timestamp(cookie["expiry"])
        
        cookie_dict = {
            "name": cookie["name"],
            "value": cookie["value"],
            "domain": ".weibo.com",
            "path": cookie["path"],
            "httpOnly": cookie.get("httpOnly", False),
            "secure": cookie.get("secure", False)
        }
        
        if "expiry" in cookie and cookie["expiry"] < int(time.time()):
            print(f"Cookie for {cookie['name']} has expired and will not be added.")
            continue
        
        if "expiry" in cookie:
            cookie_dict["expiry"] = cookie["expiry"]

        driver.add_cookie(cookie_dict)

# 打开微博主页以便加载Cookies
driver.get("https://weibo.com/")

# 加载Cookies文件
cookies_file = 'weibo_cookies.json'
add_cookies(cookies_file, driver)

# 刷新页面以应用Cookies
driver.refresh()

print("Cookies have been loaded and the page has been refreshed.")

# 微博搜索URL模板，添加时间参数
search_url_template = "https://s.weibo.com/weibo?q={query}&typeall=1&suball=1&timescope=custom%3A2024-10-01%3A2024-10-31&Refer=g"

# 实际嘉宾列表
guests = ["黄圣依", "杨子", "麦琳", "李行亮", "葛夕", "刘爽"]  # 替换为实际的嘉宾名称

# 抓取每个嘉宾的评论
all_comments = []

def scroll_page():
    """模拟用户滚动页面"""
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # 滚动到底部
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # 等待新内容加载
        time.sleep(random.uniform(2, 4))
        # 计算新高度并比较
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def fetch_comments_for_guest(guest, max_comments):
    print(f"Fetching comments for {guest}...")
    # 每次搜索前重新加载Cookies
    add_cookies(cookies_file, driver)
    driver.refresh()
    
    search_url = search_url_template.format(query=guest)
    driver.get(search_url)
    
    try:
        # 等待页面加载完成
        wait = WebDriverWait(driver, 20)  # 增加等待时间
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
        
        # 检查是否被重定向到登录页面
        if "login" in driver.current_url:
            print(f"Redirected to login page for {guest}. Please ensure Cookies are valid.")
            return
        
        # 模拟滚动页面
        scroll_page()
        
        # 查找评论元素
        comments = driver.find_elements(By.CSS_SELECTOR, 'div[node-type="like"] p[node-type="feed_list_content"].txt')
        
        for comment in comments[:max_comments]:  # 限制最多抓取max_comments条评论
            comment_text = comment.text.strip()
            all_comments.append({
                'guest': guest,
                'comment': comment_text
            })
    
    except Exception as e:
        print(f"Error fetching comments for {guest}: {e}")

for guest in guests:
    fetch_comments_for_guest(guest, 50)  # 每个人爬取50条评论

# 关闭浏览器
driver.quit()

print("All comments have been fetched.")

# 将数据存储到DataFrame
df = pd.DataFrame(all_comments)

# 保存到CSV文件
csv_filename = 'comments_october_2024.csv'
df.to_csv(csv_filename, index=False, encoding='utf-8-sig')
print(f"All comments have been saved to {csv_filename}")