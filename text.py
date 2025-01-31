from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
import time

# 设置Edge选项
edge_options = Options()
edge_options.add_argument("--headless")  # 无头模式，不打开浏览器窗口

# 创建Service对象，指定路径
service = Service(r'C:\Users\Administrator\AppData\Local\Microsoft\WindowsApps\msedgedriver.exe')

try:
    # 启动Edge浏览器
    driver = webdriver.Edge(service=service, options=edge_options)

    # 打开一个网页进行测试
    driver.get("https://www.baidu.com")

    # 等待几秒钟以确保页面加载完成
    time.sleep(5)

    # 打印页面标题以确认加载成功
    print(driver.title)

finally:
    # 关闭浏览器
    driver.quit()






