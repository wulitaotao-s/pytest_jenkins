# Test_cases/get_info.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import element_config as ec
import re
import sys
import time


def main():
    driver = None
    try:
        print("开始登录...", file=sys.stderr)
        driver = webdriver.Chrome()
        base_url = ec.url_base
        login_username = ec.login_username
        login_password = ec.login_password
        driver.get(base_url)
        wait = WebDriverWait(driver, 60)  # 增加等待时间

        # 打印当前 URL 和 title，确认是否跳转正确
        print(f"当前页面 URL: {driver.current_url}", file=sys.stderr)
        print(f"当前页面 Title: {driver.title}", file=sys.stderr)

        # 登录
        username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ec.login_username_field)))
        password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ec.login_password_field)))
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.login_submit_button)))

        username.clear()
        username.send_keys(login_username)
        password.clear()
        password.send_keys(login_password)
        button.click()

        # 等待首页加载（你的判断条件）
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".t-table")))
        print("登录成功，进入首页", file=sys.stderr)

        # 显式等待 3 秒，确保 JS 渲染完成
        time.sleep(3)

        # 获取整个 body 文本
        page_text = driver.find_element(By.TAG_NAME, "body").text

        # 提取设备信息
        device_match = re.search(r"Device\s+Type\s+(\S+)", page_text, re.IGNORECASE)
        version_match = re.search(r"Software\s+Version\s+(\S+)", page_text, re.IGNORECASE)

        device_type = device_match.group(1).strip() if device_match else "Unknown"
        software_version = version_match.group(1).strip() if version_match else "Unknown"

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