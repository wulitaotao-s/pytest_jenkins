# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import element_config as ec
import logging
from selenium.webdriver.chrome.options import Options
import re
import time
import subprocess
import sys

@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")  # 新版 Chrome 推荐写法
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    d = webdriver.Chrome(options=chrome_options)
    yield d
    d.quit()


def login(driver):
    """登录函数"""
    print("开始登录...")
    base_url = ec.url_base
    login_username = ec.login_username
    login_password = ec.login_password
    driver.get(base_url)
    wait = WebDriverWait(driver, 30)
    # 正确使用 wait.until(...)
    username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ec.login_username_field)))
    password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ec.login_password_field)))
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.login_submit_button)))
    username.clear()
    username.send_keys(login_username)
    password.clear()
    password.send_keys(login_password)
    button.click()

    # 等待首页加载
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".t-table")))
    print("登录成功，进入首页")
    
    
# 配置日志
LOG_FILE = "test_run.log"
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),  # 写入文件
        logging.StreamHandler()  # 同时输出到控制台
    ]
)

logger = logging.getLogger(__name__)


def is_switch_enabled(driver, switch_selector):
    """
    判断 t-switch 是否处于开启状态（有 t-is-checked 类）

    Args:
        driver: WebDriver 实例
        switch_selector: 开关元素的选择器（CSS 或 XPath）

    Returns:
        bool: True 表示已启用，False 表示未启用
    """
    try:
        switch = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, switch_selector))
        )
        class_name = switch.get_attribute("class")
        return "t-is-checked" in class_name
    except:
        return False


def toggle_switch(driver, switch_selector, enable=True):
    """
    控制 t-switch 开关

    Args:
        driver: WebDriver 实例
        switch_selector: 开关选择器
        enable: True=开启，False=关闭
    """
    current_state = is_switch_enabled(driver, switch_selector)
    if (enable and not current_state) or (not enable and current_state):
        switch = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, switch_selector))
        )
        switch.click()
        print(f"→ {'启用' if enable else '关闭'} WAN")


def safe_set_input_value(driver, element_selector, value):
    """
    安全地设置输入框的值（适用于 Vue/React 等受控组件）

    Args:
        driver: WebDriver 实例
        element_selector: CSS 选择器字符串
        value: 要设置的值（str）
    """
    # 等待元素存在
    elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, element_selector))
    )
    # 使用 JS 清空并赋值，同时触发 input/change 事件
    driver.execute_script("""
        const el = arguments[0];
        el.value = arguments[1];
        el.dispatchEvent(new Event('input', { bubbles: true }));
        el.dispatchEvent(new Event('change', { bubbles: true }));
    """, elem, value)


def restart_test_nic_and_ping() -> bool:
    """
    1. 使用 WMI 禁用再启用名为 'Test' 的网卡（无需管理员权限）
    2. 等待获取有效 IPv4 地址（非 169.254.x.x）
    3. 用 -S 指定源地址 ping www.jd.com
    4. 返回是否 ping 通
    """
    nic_name = "Test"

    # === 尝试导入 pywin32 ===
    try:
        import win32com.client
    except ImportError:
        print("错误: 未安装 pywin32，请运行 'pip install pywin32'", file=sys.stderr)
        return False

    # === 1. 禁用网卡（WMI）===
    print(f"→ 正在禁用网卡 '{nic_name}'...")
    try:
        wmi = win32com.client.GetObject("winmgmts:")
        disabled = False
        for nic in wmi.InstancesOf("Win32_NetworkAdapter"):
            if nic.NetEnabled and nic.Name == nic_name:
                nic.Disable()
                disabled = True
                break
        if not disabled:
            print("  (网卡可能已禁用)")
    except Exception as e:
        print(f"⚠️ 禁用失败: {e}")
        return False
    time.sleep(2)

    # === 2. 启用网卡（WMI）===
    print(f"→ 正在启用网卡 '{nic_name}'...")
    try:
        enabled = False
        for nic in wmi.InstancesOf("Win32_NetworkAdapter"):
            if not nic.NetEnabled and nic.Name == nic_name:
                nic.Enable()
                enabled = True
                break
        if not enabled:
            print("  (网卡可能已启用)")
    except Exception as e:
        print(f"启用失败: {e}")
        return False
    time.sleep(3)

    # === 3. 获取 IPv4 地址（netsh）===
    print(f"→ 等待 '{nic_name}' 获取有效 IPv4 地址...")
    ip_address = None
    for attempt in range(12):
        try:
            res = subprocess.run(
                ['netsh', 'interface', 'ip', 'show', 'config', nic_name],
                capture_output=True, text=True, timeout=10
            )
            if res.returncode == 0:
                match = re.search(r'(?:IP\s+地址|IPv4 Address):\s+(\d+\.\d+\.\d+\.\d+)', res.stdout, re.IGNORECASE)
                if match:
                    ip = match.group(1)
                    if not ip.startswith("169.254"):  # 排除 DHCP 失败地址
                        ip_address = ip
                        break
        except:
            pass
        print(f"  尝试 {attempt + 1}/12：未获取到有效 IP，等待 3 秒...")
        time.sleep(3)

    if not ip_address:
        print("超时：未能获取有效 IPv4 地址")
        return False
    print(f"获取到 IP: {ip_address}")

    # === 4. Ping 测试 ===
    print(f"→ 使用源 IP {ip_address} ping www.jd.com ...")
    ping_cmd = f'ping -S {ip_address} www.jd.com -n 4'
    try:
        res = subprocess.run(ping_cmd, shell=True, capture_output=True, text=True, timeout=30)
        stdout = res.stdout
        # 打印结果（可选，用于调试）
        print("\n" + "="*50)
        print("Ping 输出:")
        print(stdout.strip())
        print("="*50)
        if "TTL=" in stdout or "time=" in stdout:
            print("Ping 成功！")
            return True
        else:
            print("Ping 失败：无有效响应")
            return False
    except Exception as e:
        print(f"Ping 执行异常: {e}")
        return False