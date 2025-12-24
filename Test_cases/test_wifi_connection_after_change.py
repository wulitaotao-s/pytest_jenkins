import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import conftest as ct
import element_config as ec


def test_wifi_connection_after_change(driver):
    """
    验证修改 2.4G 和 5G Wi-Fi 配置后，新配置可正常连接并上网。
    步骤：
      1. 确保设备已通过 PPPoE 拨号并具备互联网访问能力
      2. 进入 2.4G Wi-Fi 页面，修改 SSID=test_@@##_2.4G，密码=@@##!!12qw，保存
      3. 使用新配置连接 2.4G Wi-Fi 并验证网络
      4. 进入 5G Wi-Fi 页面，修改 SSID=test_@@##_5G，密码=@@##!!12qw，保存
      5. 使用新配置连接 5G Wi-Fi 并验证网络
    """

    # ========== 前置：确认 PPPoE + 互联网连通性 ==========
    ct.verify_pppoe_internet_via_web_ping(driver)

    # ========== 定义新配置 ==========
    ssid_24g_new = "test_@@##_2.4G"
    password_new = "@@##!!12qw"
    ssid_5g_new = "test_@@##_5G"

    # ========== 修改并测试 2.4G Wi-Fi ==========
    print("修改 2.4G Wi-Fi 配置...")
    driver.get(ec.Basic_wifi_24G)
    wait = WebDriverWait(driver, 15)

    # 安全设置 SSID 和密码
    ct.safe_set_input_value(driver, ec.wlan_SSID, ssid_24g_new)
    ct.safe_set_input_value(driver, ec.wlan_Password, password_new)

    # 点击保存按钮
    save_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wlan_commit)))
    save_btn.click()
    print("已保存 2.4G Wi-Fi 配置，等待生效...")
    time.sleep(120)

    success_24g = ct.connect_and_test_wifi(ssid_24g_new, password_new)
    assert success_24g, f"2.4G Wi-Fi 连接或网络测试失败 (SSID: {ssid_24g_new})"

    # ========== 修改并测试 5G Wi-Fi ==========
    print("修改 5G Wi-Fi 配置...")
    driver.get(ec.Basic_wifi_5G)

    # 安全设置 SSID 和密码
    ct.safe_set_input_value(driver, ec.wlan11ac_SSID, ssid_5g_new)
    ct.safe_set_input_value(driver, ec.wlan11ac_Password, password_new)

    # 点击保存按钮
    save_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wlan11ac_commit)))
    save_btn.click()
    print("已保存 5G Wi-Fi 配置，等待生效...")
    time.sleep(120)

    success_5g = ct.connect_and_test_wifi(ssid_5g_new, password_new)
    assert success_5g, f"5G Wi-Fi 连接或网络测试失败 (SSID: {ssid_5g_new})"

    print("2.4G 和 5G Wi-Fi 修改后均验证通过")