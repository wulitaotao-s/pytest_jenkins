import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import conftest as ct
import element_config as ec


def test_reset(driver):
    # ========== 1. 登录 ==========
    ct.login(driver)

    # ========== 2. 修改 2.4G Wi-Fi ==========
    print("\n[步骤2] 修改 2.4G Wi-Fi 配置...")
    driver.get(ec.Basic_wifi_24G)
    wait = WebDriverWait(driver, 15)
    modified_24g_ssid = "test-reset-2.4G"
    modified_24g_pass = "12345678"
    ct.safe_set_input_value(driver, ec.wlan_SSID, modified_24g_ssid)
    ct.safe_set_input_value(driver, ec.wlan_Password, modified_24g_pass)

    commit_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wlan_commit)))
    commit_btn.click()
    print("已保存 2.4G Wi-Fi 配置")
    time.sleep(3)

    # ========== 3. 修改 5G Wi-Fi ==========
    print("\n[步骤3] 修改 5G Wi-Fi 配置...")
    driver.get(ec.Basic_wifi_5G)

    modified_5g_ssid = "test-reset-5G"
    modified_5g_pass = "12345678"

    ct.safe_set_input_value(driver, ec.wlan11ac_SSID, modified_5g_ssid)
    ct.safe_set_input_value(driver, ec.wlan11ac_Password, modified_5g_pass)

    commit_btn_5g = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wlan11ac_commit)))
    commit_btn_5g.click()
    print("已保存 5G Wi-Fi 配置")
    time.sleep(3)

    # ========== 4. 执行 Factory Reset ==========
    print("\n[步骤4] 进入设备管理界面，执行 Reset...")
    driver.get(ec.Advanced_System_Upgrade)

    reset_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.Device_Management_Reset)))
    reset_btn.click()

    confirm_reset_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.Device_confirmReset)))
    confirm_reset_btn.click()
    ct.save_screenshot_and_log(driver)
    print("已确认 Reset，设备将重启...")

    # ========== 5. 等待设备重启并重新上线 ==========
    print("\n[步骤5] 等待设备重启并重新上线...")
    time.sleep(60)  # 给设备关机时间
    ct.wait_for_device_online(ec.url_base, timeout=150)

    # ========== 6. 重新登录（此时可能进入向导界面）==========
    print("\n[步骤6] 重新登录设备...")
    ct.login(driver)

    # ========== 7. 检查 Wi-Fi 配置是否恢复默认 ==========
    print("\n[步骤7] 检查 Reset 后的 Wi-Fi 配置...")

    # 检查 2.4G
    driver.get(ec.Basic_wifi_24G)
    ssid_24g_after = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ec.wlan_SSID))).get_attribute("value").strip()
    password_24g_after = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ec.wlan_Password))).get_attribute("value").strip()
    ct.save_screenshot_and_log(driver)

    # 检查 5G
    driver.get(ec.Basic_wifi_5G)
    ssid_5g_after = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ec.wlan11ac_SSID))).get_attribute("value").strip()
    password_5g_after = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ec.wlan11ac_Password))).get_attribute("value").strip()
    ct.save_screenshot_and_log(driver)

    print("\n【Reset 后实际配置】")
    print(f"2.4G SSID: '{ssid_24g_after}'")
    print(f"2.4G 密码: '{password_24g_after}'")
    print(f"5G   SSID: '{ssid_5g_after}'")
    print(f"5G   密码: '{password_5g_after}'")

    # ========== 8. 判断是否恢复默认 ==========


    is_24g_restored = (ssid_24g_after != modified_24g_ssid) or (password_24g_after != modified_24g_pass)
    is_5g_restored = (ssid_5g_after != modified_5g_ssid) or (password_5g_after != modified_5g_pass)

    print("\n【验证结果】")
    print(f"2.4G 是否恢复默认？ {'是' if is_24g_restored else '否'}")
    print(f"5G   是否恢复默认？ {'是' if is_5g_restored else '否'}")

    if is_24g_restored and is_5g_restored:
        print("\n测试通过：Reset 成功恢复默认 Wi-Fi 配置")
        assert True
    else:
        print("\n测试失败：Reset 后 Wi-Fi 配置仍为修改后的值！")
        if not is_24g_restored:
            print(f"  → 2.4G 未恢复：SSID='{ssid_24g_after}', 密码='{password_24g_after}'")
        if not is_5g_restored:
            print(f"  → 5G 未恢复：SSID='{ssid_5g_after}', 密码='{password_5g_after}'")
        assert False, "Factory Reset 未清除自定义 Wi-Fi 配置"




