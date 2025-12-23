import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import login
import element_config as ec


def wait_for_device_online(base_url, timeout=150):
    """等待设备重启完成，直到能访问 base_url"""
    print(f"等待设备重启（最多 {timeout} 秒）...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # 尝试发起 HTTP 请求（不加载完整页面，更快）
            response = requests.get(ec.url_base, timeout=3)
            if response.status_code == 200:
                print("设备已在线，开始登录...")
                return True
        except Exception:
            pass
        time.sleep(5)
        elapsed = int(time.time() - start_time)
        print(f"已等待 {elapsed} 秒...")
    raise TimeoutError(f"设备在 {timeout} 秒内未恢复在线")


def parse_online_time(online_time_str):
    """
    解析 Online Time 字符串，如 "2m 30s" 或 "1h 10m"
    返回总秒数
    """
    online_time_str = online_time_str.strip()
    total_seconds = 0

    if 'h' in online_time_str:
        h_part = online_time_str.split('h')[0].strip()
        total_seconds += int(h_part) * 3600
        online_time_str = online_time_str.split('h', 1)[1].strip()

    if 'm' in online_time_str:
        m_part = online_time_str.split('m')[0].strip()
        total_seconds += int(m_part) * 60
        online_time_str = online_time_str.split('m', 1)[1].strip()

    if 's' in online_time_str:
        s_part = online_time_str.split('s')[0].strip()
        if s_part.isdigit():
            total_seconds += int(s_part)

    return total_seconds


def test_device_reboot(driver):
    # ========== 1. 登录 ==========
    login(driver)

    # ========== 2. 进入 Device Management 页面 ==========
    print("跳转到 Device Management 页面")
    driver.get(ec.Advanced_System_Upgrade)
    wait = WebDriverWait(driver, 15)

    # ========== 3. 点击 Restart ==========
    print("点击 Restart 按钮")
    reboot_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.Device_Management_Restart)))
    reboot_btn.click()

    # ========== 4. 点击 Confirm Reboot ==========
    print("点击确认重启")
    confirm_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.Device_confirmReboot)))
    confirm_btn.click()

    # ========== 5. 等待设备重启 ==========
    print("等待设备重启...")
    time.sleep(30)  # 给设备一点关机时间
    wait_for_device_online(ec.url_base, timeout=150)

    # ========== 6. 重新登录并进入 Home 页面 ==========
    print("设备已恢复，重新登录...")
    login(driver)
    driver.get(ec.home)
    time.sleep(3)

    # ========== 7. 获取 Online Time 并验证 ==========
    print("获取 Online Time...")

    try:
        # 使用 XPath 精准定位 "Online Time" 行
        online_time_row = wait.until(
            EC.presence_of_element_located((
                By.XPATH,
                "//tr[td[text()='Online Time']]"
            ))
        )

        # 获取 "Online Time" 所在行的第二个 td（即值）
        value_cell = online_time_row.find_elements(By.TAG_NAME, "td")[1]
        online_time_text = value_cell.text.strip()
        print(f"Online Time: {online_time_text}")

        # 使用正则解析时间格式：如 "1 min 40 s"
        import re
        match = re.match(r'(\d+)\s*min\s*(\d+)\s*s', online_time_text, re.IGNORECASE)
        if not match:
            raise Exception(f"无法解析 Online Time 格式: {online_time_text}")

        mins = int(match.group(1))
        secs = int(match.group(2))
        total_seconds = mins * 60 + secs

        print(f"解析为总秒数: {total_seconds} 秒")

        if total_seconds < 180:  # 3分钟 = 180秒
            print("Online Time < 3m，重启验证通过！")
        else:
            print(f"Online Time >= 3m ({total_seconds}s)，可能不是刚重启！")
            assert False, f"Online Time 为 {online_time_text}，超过 3 分钟"

    except Exception as e:
        print(f"获取或解析 Online Time 失败: {e}")
        # 打印页面内容用于调试
        body_text = driver.find_element(By.TAG_NAME, "body").text[:500]
        print(f"页面前500字符: {body_text}")
        assert False, "无法验证 Online Time"





# ========== 主程序（可选，用于独立运行） ==========
if __name__ == "__main__":
    driver = webdriver.Chrome()
    try:
        test_device_reboot(driver)
    finally:
        driver.quit()