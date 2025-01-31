import json
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

# 设置Edge选项
edge_options = Options()
# 如果需要无头模式，取消下面的注释
# edge_options.add_argument("--headless")
edge_options.add_argument("--disable-gpu")
edge_options.add_argument("--no-sandbox")
edge_options.add_argument("--disable-dev-shm-usage")

# 创建Service对象，指定路径（如果不在系统PATH中）
service_path = r'C:\Users\Administrator\AppData\Local\Microsoft\WindowsApps\msedgedriver.exe'  # 替换为你的msedgedriver路径
service = Service(service_path)

# 启动Edge浏览器
driver = webdriver.Edge(service=service, options=edge_options)

# 打开已登录的微博页面
driver.get("https://weibo.com/")

input("请在浏览器中手动登录微博，然后按回车键继续...")

# 保存Cookies到文件
cookies = driver.get_cookies()
with open('weibo_cookies.json', 'w') as f:
    json.dump(cookies, f, indent=4)

print("Cookies已保存到weibo_cookies.json文件中")

# 关闭浏览器
driver.quit()





















