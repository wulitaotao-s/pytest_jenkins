import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import conftest as ct
import element_config as ec



def test_wifi_init_status(driver):
    """
    验证设备出厂重置后，2.4G 和 5G Wi-Fi 配置正确且可连接上网。
    前提：设备已通过 PPPoE 拨号并具备互联网访问能力。
    步骤：
      1. 验证当前 PPPoE + 互联网连通性（通过 Web Ping）
      2. 登录 Web 管理界面
      3. 获取 2.4G SSID/密码，执行连接测试
      4. 获取 5G SSID/密码，执行连接测试
    """
    # ========== 关键前置：确认 PPPoE 拨号成功且可上网 ==========
    ct.verify_pppoe_internet_via_web_ping(driver)

    # ========== 正式 Wi-Fi 验证 ==========
    # 测试 2.4G Wi-Fi
    driver.get(ec.Basic_wifi_24G)
    ssid_24g = ct.wait_for_non_empty_value(driver, ec.wlan_SSID)
    password_24g = ct.wait_for_non_empty_value(driver, ec.wlan_Password)
    print(f"2.4G Wi-Fi 配置: SSID={ssid_24g}, Password={password_24g}")
    ct.save_screenshot_and_log(driver)
    success_24g = ct.connect_and_test_wifi(ssid_24g, password_24g)
    assert success_24g, f"2.4G Wi-Fi 连接或网络测试失败 (SSID: {ssid_24g})"

    # 测试 5G Wi-Fi
    driver.get(ec.Basic_wifi_5G)
    ssid_5g = ct.wait_for_non_empty_value(driver, ec.wlan11ac_SSID)
    password_5g = ct.wait_for_non_empty_value(driver, ec.wlan11ac_Password)
    print(f"5G Wi-Fi 配置: SSID={ssid_5g}, Password={password_5g}")
    ct.save_screenshot_and_log(driver)
    success_5g = ct.connect_and_test_wifi(ssid_5g, password_5g)
    assert success_5g, f"5G Wi-Fi 连接或网络测试失败 (SSID: {ssid_5g})"

    print("2.4G 和 5G Wi-Fi 均验证通过")