# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import element_config as ec
import logging
import os


@pytest.fixture(scope="function")
def driver():
    """启动浏览器，测试结束后自动关闭"""
    d = webdriver.Chrome()
    yield d
    d.quit()

def login(driver):
    """登录函数"""
    print("开始登录...")
    print("开始登录...")
    base_url = ec.base_url
    login_username = ec.login_username
    login_password = ec.login_password

    driver.get(base_url)
    wait = WebDriverWait(driver, 10)

    # ✅ 正确使用 wait.until(...)
    username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ec.login_username_field)))
    password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ec.login_password_field)))
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.login_submit_button)))

    username.clear()
    username.send_keys(login_username)
    password.clear()
    password.send_keys(login_password)
    button.click()

    # 等待首页加载
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".t-table")))
    print("登录成功，进入首页")
    
    
# 配置日志
LOG_FILE = "test_run.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),  # 写入文件
        logging.StreamHandler()  # 同时输出到控制台
    ]
)

logger = logging.getLogger(__name__)
