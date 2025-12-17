# conftest.py

import os
import sys
from datetime import datetime
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoAlertPresentException
import element_config as ec

@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--disable-popup-blocking")
    # 注意：调试时不要加 --headless

    driver = webdriver.Chrome(options=chrome_options)
    yield driver
    driver.quit()


def login(driver):
    driver.get(ec.base_url)
    wait = WebDriverWait(driver, 10)

    username_input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ec.login_username)))
    password_input = driver.find_element(By.CSS_SELECTOR, ec.login_password)
    login_button = driver.find_element(By.CSS_SELECTOR, ec.login_commit)

    username_input.clear()
    username_input.send_keys("admin")
    password_input.clear()
    password_input.send_keys("admin")
    login_button.click()

    # 等待可能的弹窗（隐形 alert）
    import time
    time.sleep(1.5)
    try:
        alert = driver.switch_to.alert
        print(f"登录后自动关闭弹窗: {alert.text}")
        alert.accept()
    except NoAlertPresentException:
        pass

    # 等待首页加载
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".t-table")))


# ========================
# 🔹 独立日志保存函数（供测试类调用）
# ========================
def save_test_log(content: str) -> str:
    """
    将测试日志保存到 D:\pytest_jenkins\report\YYYY-MM-DD HH:MM:SS.log
    返回完整文件路径
    """
    log_dir = r"D:\pytest_jenkins\report"
    os.makedirs(log_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = os.path.join(log_dir, f"{timestamp}.log")

    with open(log_file, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f"日志已保存至: {log_file}")
    return log_file
    
@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    print(f"开始执行测试: {item.name}")