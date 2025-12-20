# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import element_config as ec
import logging
import subprocess
import time
import re



@pytest.fixture(scope="function")
def driver():
    """启动浏览器，测试结束后自动关闭"""
    d = webdriver.Chrome()
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
    1. 禁用再启用名为 'Test' 的网卡
    2. 等待其获取 IPv4 地址（使用 netsh 查询）
    3. 使用 -S 指定源地址 ping www.jd.com
    4. 返回是否 ping 通
    """
    nic_name = "Test"

    def run_cmd(cmd, shell=True):
        result = subprocess.run(cmd, shell=shell, capture_output=True, text=True)
        return result

    # === 1. 禁用网卡 ===
    print(f"→ 正在禁用网卡 '{nic_name}'...")
    res = run_cmd(f'netsh interface set interface "{nic_name}" admin=disabled')
    if res.returncode != 0:
        print(f"❌ 禁用失败: {res.stderr.strip()}")
        return False
    time.sleep(3)

    # === 2. 启用网卡 ===
    print(f"→ 正在启用网卡 '{nic_name}'...")
    res = run_cmd(f'netsh interface set interface "{nic_name}" admin=enabled')
    if res.returncode != 0:
        print(f"❌ 启用失败: {res.stderr.strip()}")
        return False
    time.sleep(5)  # 给 DHCP 时间获取地址

    # === 3. 获取该网卡的 IPv4 地址（使用 netsh）===
    print(f"→ 正在获取 '{nic_name}' 的 IPv4 地址...")
    for attempt in range(10):
        res = run_cmd(f'netsh interface ip show config "{nic_name}"')
        if res.returncode != 0:
            print("无法运行 netsh")
            return False

        # 匹配 IPv4 地址：支持中英文显示
        # 中文：IP 地址: 192.168.10.2
        # 英文：IPv4 Address: 192.168.10.2
        match = re.search(r'(?:IP 地址|IPv4 Address):\s+(\d+\.\d+\.\d+\.\d+)', res.stdout, re.IGNORECASE)
        if match:
            ip_address = match.group(1)
            print(f"✅ 成功获取 IP: {ip_address}")
            break
        else:
            print(f"⏳ 尝试 {attempt + 1}/10：未获取到 IP，等待 3 秒...")
            time.sleep(3)
    else:
        print("❌ 超时：未能获取到 IPv4 地址")
        return False
    # === 4. 使用 -S 指定源地址 ping www.jd.com ===
    print(f"→ 使用源 IP {ip_address} ping www.jd.com ...")
    ping_cmd = f'ping -S {ip_address} www.jd.com -n 4'
    res = run_cmd(ping_cmd)

    # 🔹 完整打印 ping 的输出（stdout + stderr）
    print("\n" + "="*60)
    print("Ping 命令执行结果:")
    print("="*60)
    if res.stdout.strip():
        print(res.stdout)
    if res.stderr.strip():
        print("标准错误输出（stderr）:")
        print(res.stderr)
    print("="*60)

    # === 5. 判断是否 ping 通 ===
    if "TTL=" in res.stdout or "time=" in res.stdout:
        print(" Ping 成功！")
        return True
    else:
        print(" Ping 失败：未收到有效响应")
        return False