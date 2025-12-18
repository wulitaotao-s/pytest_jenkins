# download_all_pages_html.py
import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

GATEWAY_URL = "http://192.168.10.1"
USERNAME = "admin"
PASSWORD = "admin"

OUTPUT_DIR = "downloaded_html_pages"
os.makedirs(OUTPUT_DIR, exist_ok=True)

PAGE_PATHS = [
    "/index.html",
    "/index.html#/basic/wan",
    "/index.html#/basic/lan",
    "/index.html#/basic/cwmp",
    "/index.html#/basic/voip",
    "/index.html#/basic/iptv",
    "/index.html#/basic/wifi",
    "/index.html#/basic/wifi/bandsteer",
    "/index.html#/basic/wifi/wifi24",
    "/index.html#/basic/wifi/wifi5",
    "/index.html#/basic/wifi/wps",
    "/index.html#/basic/wifi/guest",
    "/index.html#/basic/device",
    "/index.html#/basic/parentalControl",
    "/index.html#/basic/mode",
    "/index.html#/basic/EasyMesh",
    "/index.html#/advanced/network/qos",
    "/index.html#/advanced/network/upnp",
    "/index.html#/advanced/network/ddns",
    "/index.html#/advanced/network/staticRoute",
    "/index.html#/advanced/network/binding",
    "/index.html#/advanced/network/vpn/ipSec",
    "/index.html#/advanced/network/vpn/l2tp",
    "/index.html#/advanced/user/Firewall",
    "/index.html#/advanced/user/macFilter",
    "/index.html#/advanced/user/urlFilter",
    "/index.html#/advanced/user/portFilter",
    "/index.html#/advanced/user/portForward",
    "/index.html#/advanced/user/dmz",
    "/index.html#/advanced/user/alg",
    "/index.html#/advanced/user/aclFilter",
    "/index.html#/advanced/system/password",
    "/index.html#/advanced/system/upgrade",
    "/index.html#/advanced/system/autoReboot",
    "/index.html#/advanced/system/timeSetting",
    "/index.html#/advanced/system/systemTest",
    "/index.html#/advanced/system/device",
    "/index.html#/advanced/system/ledCtrl",
    "/index.html#/advanced/system/loopBack",
    "/index.html#/advanced/system/test",
    "/index.html#/advanced/system/ponAuth",
    "/index.html#/advanced/system/telnet",
    "/index.html#/hidePage",
]

LOGIN_USERNAME_SELECTOR = 'input[placeholder="Please Enter Your Username"]'
LOGIN_PASSWORD_SELECTOR = 'input[placeholder="Please Enter Your Password"]'
LOGIN_SUBMIT_SELECTOR = "button[type='submit']"

def create_driver(headless=False):
    options = Options()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--ignore-certificate-errors")
    options.add_experimental_option("excludeSwitches", ["enable-logging"])
    return webdriver.Chrome(options=options)

def sanitize_filename(url_path):
    name = url_path.replace("/index.html#/", "").replace("/", "_").replace("#", "")
    if not name or name == "index.html":
        name = "home"
    return name + ".html"

def wait_for_page_load(driver, timeout=8):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.menu-item, .t-form, .t-card, #network"))
        )
    except:
        pass
    time.sleep(1.5)

def main():
    driver = create_driver(headless=False)
    try:
        print("正在访问网关登录页...")
        driver.get(GATEWAY_URL)

        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, LOGIN_USERNAME_SELECTOR))
        )
        print("登录框已就绪")

        driver.find_element(By.CSS_SELECTOR, LOGIN_USERNAME_SELECTOR).send_keys(USERNAME)
        driver.find_element(By.CSS_SELECTOR, LOGIN_PASSWORD_SELECTOR).send_keys(PASSWORD)
        driver.find_element(By.CSS_SELECTOR, LOGIN_SUBMIT_SELECTOR).click()

        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.menu-item, .t-layout, #network"))
            )
            print("登录成功，进入主界面")
        except TimeoutException:
            print("登录失败：未检测到首页元素，请检查账号密码或网络连接")
            return

        total = len(PAGE_PATHS)
        for i, path in enumerate(PAGE_PATHS, 1):
            full_url = GATEWAY_URL + path
            filename = sanitize_filename(path)
            filepath = os.path.join(OUTPUT_DIR, filename)

            print(f"[{i}/{total}] 访问: {full_url}")
            try:
                driver.get(full_url)
                wait_for_page_load(driver)

                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                print(f"  保存: {filename}")

            except Exception as e:
                error_file = filepath.replace(".html", "_ERROR.html")
                with open(error_file, "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
                print(f"  失败（已保存错误页）: {e}")

        print(f"全部 {total} 个页面 HTML 已保存至: {os.path.abspath(OUTPUT_DIR)}")

    finally:
        driver.quit()

if __name__ == "__main__":
    main()