# Test_cases/get_info.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import element_config as ec
import re
import sys

def main():
    driver = None
    try:
        driver = webdriver.Chrome()
        print("开始登录...", file=sys.stderr)

        base_url = ec.url_base
        login_username = ec.login_username
        login_password = ec.login_password

        driver.get(base_url)
        wait = WebDriverWait(driver, 30)

        # 登录
        username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ec.login_username_field)))
        password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ec.login_password_field)))
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.login_submit_button)))

        username.clear()
        username.send_keys(login_username)
        password.clear()
        password.send_keys(login_password)
        button.click()

        # 等待首页加载完成（你已有的判断）
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".t-table")))
        print("登录成功，进入首页", file=sys.stderr)

        # 获取整个页面文本
        page_text = driver.find_element(By.TAG_NAME, "body").text

        # 使用正则提取 Device Type 和 Software Version
        device_match = re.search(r"Device\s+Type\s*[:：]?\s*([A-Z0-9\-_]+)", page_text, re.IGNORECASE)
        version_match = re.search(r"Software\s+Version\s*[:：]?\s*([A-Za-z0-9\.\-_]+)", page_text, re.IGNORECASE)

        device_type = device_match.group(1).strip() if device_match else "Unknown"
        software_version = version_match.group(1).strip() if version_match else "Unknown"

        # 关键：只输出这两行标准输出，供 Jenkins 捕获
        print(f"Device Type: {device_type}")
        print(f"Software Version: {software_version}")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        print("Device Type: Unknown")
        print("Software Version: Unknown")
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    main()