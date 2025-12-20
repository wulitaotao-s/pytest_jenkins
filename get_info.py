# get_info.py
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import element_config as ec
import sys, time

def main():
    driver = None
    try:
        print("开始登录...", file=sys.stderr)
        driver = webdriver.Chrome()
        driver.get(ec.url_base)

        # 登录逻辑不变
        wait = WebDriverWait(driver, 60)
        username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ec.login_username_field)))
        password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ec.login_password_field)))
        button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.login_submit_button)))

        username.clear()
        username.send_keys(ec.login_username)
        password.clear()
        password.send_keys(ec.login_password)
        button.click()

        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".t-table")))
        print("登录成功，进入首页", file=sys.stderr)

        # 获取整个页面内容（HTML + 文本）
        page_html = driver.page_source
        page_text = driver.find_element(By.TAG_NAME, "body").text

        # === 调试：打印真实内容（只输出到 stderr，不影响 Jenkins 捕获 stdout）===
        print("=== 页面原始文本 ===", file=sys.stderr)
        print(page_text[:500], file=sys.stderr)  # 前 500 字足够看结构

        # ✅ 最简正则：匹配 "Device Type XXX" 和 "Software Version YYY"
        device_match = re.search(r"Device\s+Type\s+(\S+)", page_text, re.IGNORECASE)
        version_match = re.search(r"Software\s+Version\s+(\S+)", page_text, re.IGNORECASE)

        device_type = device_match.group(1).strip() if device_match else "Unknown"
        software_version = version_match.group(1).strip() if version_match else "Unknown"

        # ✅ 只有这两行输出到 stdout，供 Jenkins 捕获
        print(f"Device Type: {device_type}")
        print(f"Software Version: {software_version}")

    except Exception as e:
        print(f"Error in get_info: {e}", file=sys.stderr)
        print("Device Type: Unknown")
        print("Software Version: Unknown")
    finally:
        if driver:
            driver.quit()

if __name__ == '__main__':
    main()