from selenium.webdriver.common.by import By
import conftest as ct
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import element_config as ec
import time


def test_get_base_info(driver):
    """
    获取基础信息：依次进入 Device Information、PON Information、2.4G WiFi Info、5G WiFi Info 页面并截图，
    截图文件名严格按页面标题命名。
    """

    # ========== 1. 登录 ==========
    ct.login(driver)

    wait = WebDriverWait(driver, 10)

    # ========== 2. Device Information ==========
    print("跳转到 Device Information 页面")
    driver.get(ec.home)
    device_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.DeviceName)))
    device_btn.click()
    time.sleep(1)

    dev_info_tab = wait.until(EC.element_to_be_clickable((By.XPATH, ec.Device_Information)))
    dev_info_tab.click()
    time.sleep(2)
    # 重命名截图
    ct.save_screenshot_and_log(driver)

    # ========== 3. PON Information ==========
    print("跳转到 PON Information 页面")
    pon_tab = wait.until(EC.element_to_be_clickable((By.XPATH, ec.PON_Information)))
    pon_tab.click()
    time.sleep(2)
    ct.save_screenshot_and_log(driver)

    # ========== 4. 2.4G WiFi Info ==========
    print("跳转到 2.4G WiFi Info 页面")
    driver.get(ec.Basic_wifi_24G)
    time.sleep(2)
    ct.save_screenshot_and_log(driver)

    # ========== 5. 5G WiFi Info ==========
    print("跳转到 5G WiFi Info 页面")
    driver.get(ec.Basic_wifi_5G)
    time.sleep(2)
    ct.save_screenshot_and_log(driver)
    print("基础信息截图完成")