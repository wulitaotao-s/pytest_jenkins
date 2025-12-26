# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import element_config as ec
from selenium.webdriver.chrome.options import Options
import sys, datetime, subprocess, tempfile, os, re, time, requests, inspect
from datetime import datetime
from threading import Lock


# 全局状态
_ROOT_DIR = None          # 例如: D:\...\photo_2025-10-01
_CREATED_SCRIPT_DIRS = set()  # 已创建的脚本子目录名集合
_LOCK = Lock()
BASE_PARENT = r"D:\pytest_jenkins_test@tmp"


@pytest.fixture(scope="function")
def driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    d = webdriver.Chrome(options=chrome_options)
    # d = webdriver.Chrome()
    yield d
    d.quit()


def login(driver):
    """
    登录函数，确保使用英文界面。
    如果检测到非英文，会关闭当前 driver，新建一个并重试。
    返回：新的 driver 实例（可能已替换）
    """
    print("开始登录流程...")
    wait = WebDriverWait(driver, 30)
    driver.get(ec.url_base)

    # ========== 1 检查语言 ==========
    lang_button = wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ec.login_language))
    )
    current_text = lang_button.text.strip()
    print(f"检测到当前语言: '{current_text}'")
    if current_text != "English":
        print("→ 非英文界面，正在切换为 English...")
        lang_button.click()
        # 等待下拉菜单
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".t-dropdown__menu")))
        # 点击 English
        english_elem = wait.until(
            EC.element_to_be_clickable((By.XPATH, ec.english_option))
        )
        english_elem.click()
        print("→ 已点击 English，等待 2 秒后重启浏览器以确保干净环境...")
        time.sleep(2)
    driver.get(ec.url_base)

    # ========== 2. 登录 ==========
    username = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ec.login_username_field)))
    password = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ec.login_password_field)))
    button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.login_submit_button)))

    username.send_keys(ec.login_username)
    password.send_keys(ec.login_password)
    button.click()

    # ========== 3. 尝试检测是否在向导界面（通过是否存在 guide_skip 按钮） ==========
    try:
        # 等待最多 5 秒看是否有向导的 Skip 按钮
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ec.guide_skip))
        )
        print("→ 检测到向导界面，正在自动跳过设置...")
        handle_guide_wizard(driver)
        print("向导处理完成，已进入主界面")
    except:
        # 没有向导，说明直接进了首页
        print("→ 未检测到向导界面，等待首页加载...")
    # 等待首页加载
    print("登录成功，进入首页")


def wait_for_device_online(base_url, timeout=150):
    """等待设备重启完成，直到能访问 base_url"""
    print(f"等待设备重启（最多 {timeout} 秒）...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            response = requests.get(base_url, timeout=3)
            if response.status_code == 200:
                print("设备已在线")
                return True
        except Exception:
            pass
        time.sleep(5)
        elapsed = int(time.time() - start_time)
        print(f"已等待 {elapsed} 秒...")
    raise TimeoutError(f"设备在 {timeout} 秒内未恢复在线")


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
        print(f"禁用失败: {e}")
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


def connect_and_test_wifi(ssid: str, password: str) -> bool:
    """直接连接指定 Wi-Fi 并测试网络连通性（无扫描，适配中文 Windows）"""
    profile_name = f"__TEMP_{ssid}"
    tmp_path = None
    ip_address = None
    ping_output = ""
    test_passed = False

    try:
        print(f"[INFO] 跳过扫描，直接尝试连接 Wi-Fi: '{ssid}'")

        # 断开当前连接
        print("[INFO] 断开当前 Wi-Fi 连接...")
        subprocess.run('netsh wlan disconnect', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # 创建临时配置文件（WPA2-PSK + AES）
        xml_content = f'''<?xml version="1.0"?>
<WLANProfile xmlns="http://www.microsoft.com/networking/WLAN/profile/v1">
    <name>{profile_name}</name>
    <SSIDConfig>
        <SSID><name>{ssid}</name></SSID>
    </SSIDConfig>
    <connectionType>ESS</connectionType>
    <MSM>
        <security>
            <authEncryption>
                <authentication>WPA2PSK</authentication>
                <encryption>AES</encryption>
                <useOneX>false</useOneX>
            </authEncryption>
            <sharedKey>
                <keyType>passPhrase</keyType>
                <protected>false</protected>
                <keyMaterial>{password}</keyMaterial>
            </sharedKey>
        </security>
    </MSM>
</WLANProfile>'''

        with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False, encoding='utf-8-sig') as f:
            f.write(xml_content)
            tmp_path = f.name

        # 添加配置（使用 gbk 编码）
        print("[INFO] 添加临时 Wi-Fi 配置文件...")
        add_result = subprocess.run(
            f'netsh wlan add profile filename="{tmp_path}"',
            shell=True,
            capture_output=True,
            text=True,
            encoding='gbk'  # ← 关键：中文系统必须用 gbk
        )
        if add_result.returncode != 0:
            print(f"[ERROR] 添加 Wi-Fi 配置失败:\n{add_result.stderr}")
            return False

        # 发起连接（使用 gbk 编码）
        print("[INFO] 发起 Wi-Fi 连接...")
        connect_result = subprocess.run(
            f'netsh wlan connect name="{profile_name}"',
            shell=True,
            capture_output=True,
            text=True,
            encoding='gbk',
            timeout=30
        )
        if connect_result.returncode != 0:
            print(f"[ERROR] Wi-Fi 连接命令失败:\n{connect_result.stderr}")
            return False

        # 等待获取有效 IPv4 地址（最多 20 秒）
        print("[INFO] 等待获取有效 IPv4 地址（最多 20 秒）...")
        for _ in range(20):
            try:
                output = subprocess.check_output('ipconfig', shell=True, text=True, encoding='gbk')  # ← gbk
                current_adapter = None
                for line in output.splitlines():
                    if '适配器' in line or 'Adapter' in line:
                        if ':' in line:
                            current_adapter = line.strip().rstrip(':')
                        continue
                    if current_adapter and any(kw in current_adapter for kw in ['WLAN', '无线', 'Wi-Fi', 'Wireless']):
                        if 'IPv4 地址' in line or 'IPv4 Address' in line:
                            match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', line)
                            if match:
                                ip = match.group()
                                if not ip.startswith('169.254.') and ip != '0.0.0.0':
                                    ip_address = ip
                                    break
                if ip_address:
                    break
            except Exception:
                pass
            time.sleep(1)

        if ip_address:
            print(f"[SUCCESS] 获取到有效 IP: {ip_address}")
        else:
            print("[ERROR] 20 秒内未获取到有效 IP 地址")

        # 执行 Ping 测试（使用 gbk 编码）
        if ip_address:
            ping_cmd = f'ping -n 3 -S {ip_address} www.jd.com'
            print(f"[INFO] 执行 Ping: {ping_cmd}")
            try:
                result = subprocess.run(
                    ping_cmd,
                    shell=True,
                    capture_output=True,
                    text=True,
                    encoding='gbk',  # ← gbk
                    timeout=10
                )
                ping_output = (result.stdout or result.stderr).strip()

                # 健壮判断：必须有 TTL= 且无“请求超时”或“无法访问”
                if ('TTL=' in ping_output and
                    '无法访问' not in ping_output and
                    'Destination host unreachable' not in ping_output):
                    test_passed = True
                else:
                    test_passed = False
            except Exception as e:
                ping_output = f"Ping 异常: {e}"
                test_passed = False
        else:
            ping_output = "跳过 Ping（无有效 IP）"

        print("Ping 结果:")
        print(ping_output)

    except Exception as e:
        print(f"[CRITICAL] 函数执行异常: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        # 清理：断开并删除临时配置
        print("[CLEANUP] 清理临时配置...")
        subprocess.run('netsh wlan disconnect', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(f'netsh wlan delete profile name="{profile_name}"', shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except OSError:
                pass

    print(f"[RESULT] 整体测试 {'通过' if test_passed else '失败'}")
    return test_passed


def wait_for_non_empty_value(driver, selector, timeout=15):
    """
    等待指定 CSS 选择器的元素存在，并且其 value 属性非空。
    返回该 value 字符串。
    """
    wait = WebDriverWait(driver, timeout)
    elem = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
    for _ in range(timeout):
        value = elem.get_attribute("value").strip()
        if value:
            return value
        time.sleep(1)
    assert False, f"元素 {selector} 的 value 在 {timeout} 秒内未被填充"


def verify_pppoe_internet_via_web_ping(driver):
    """
    内部函数：通过 Web 界面 Ping www.jd.com 验证 PPPoE 拨号后互联网是否可达。
    不修改配置，仅验证当前状态。
    """
    """测试 WAN PPPoE 模式 + Ping www.jd.com 连通性"""
    # ========== 1. 登录 ==========
    login(driver)

    # ========== 2. 进入 Basic > WAN 页面 ==========
    print(" 跳转到 WAN 配置页面")
    driver.get(ec.Basic_wan)
    wait = WebDriverWait(driver, 15)

    # ========== 3. 配置 WAN 为 PPPoE 模式 ==========
    print(" 配置 WAN 为 PPPoE 模式")

    # 选择 Request Name: 2_INTERNET_R_VID_100
    request_name_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Request_Name)))
    request_name_input.click()
    internet_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Request_Name_INTERNET)))
    internet_option.click()

    # 设置 Access Type = Route
    access_type_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Access_Type)))
    access_type_input.click()
    route_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Access_Type_Route)))
    route_option.click()

    # 设置 Connection Mode = PPPoE
    conn_mode_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Connection_Mode)))
    conn_mode_input.click()
    pppoe_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Connection_Mode_PPPoE)))
    pppoe_option.click()

    # 设置 Username 和 Password
    print(" 设置 PPPoE 用户名和密码")
    safe_set_input_value(driver, ec.wan_pppoe_name, "PPPOE")  # 示例值，请替换为实际账号
    safe_set_input_value(driver, ec.wan_pppoe_password, "PPPOE")  # 示例值，请替换为实际密码

    # 设置 VLAN ID = 100
    print(" 设置 VLAN ID = 100")
    safe_set_input_value(driver, ec.wan_VLAN_ID, "100")

    # 设置 MTU = 1500
    print(" 设置 MTU = 1500")
    safe_set_input_value(driver, ec.wan_MTU, "1500")

    # 启用 Nat Enable 开关
    switch = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_nat_enable)))
    if "t-is-checked" not in switch.get_attribute("class"):
        switch.click()
        print(" 启用 Nat Enable")
    else:
        print(" Nat Enable 已启用")

    # 设置 Protocol Version = IPv4/IPv6
    ipv4_ipv6_radio = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_ipv4ipv6)))
    if not ipv4_ipv6_radio.is_selected():
        ipv4_ipv6_radio.click()
        print(" 设置协议版本为 IPv4/IPv6")

    # 设置 Connection Mode = DHCPv6（可选，根据设备）
    dhcpv6_option_list = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_IPv6_Connection_Mode)))
    dhcpv6_option_list.click()
    dhcpv6_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_IPv6_Connection_Mode_DHCP)))
    dhcpv6_option.click()

    # 启用 WAN 开关
    switch = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Enable)))
    if "t-is-checked" not in switch.get_attribute("class"):
        switch.click()
        print(" 启用 WAN")
    else:
        print(" WAN 已启用")

    # 保存配置
    print(" 保存 WAN 配置")
    save_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_commit)))
    save_btn.click()
    time.sleep(15)

    # ========== 4. 执行 Ping 测试 ==========
    print(" 跳转到系统测试页面")
    driver.get(ec.Advanced_System_System_Test)
    wait = WebDriverWait(driver, 15)

    # 设置 Ping 次数
    safe_set_input_value(driver, ec.System_Test_Ping_Repeat_Times, "3")

    # 选择接口：Internet
    print(" 选择 Ping 接口 = Internet")
    interface_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.System_Test_Ping_Interface)))
    driver.execute_script("arguments[0].click();", interface_input)
    internet_opt = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.System_Test_Ping_INTERNET)))
    internet_opt.click()

    # 设置目标地址
    print(" 设置 Ping 目标地址 = www.jd.com")
    safe_set_input_value(driver, ec.System_Test_Ping_Address, "www.jd.com")

    # 点击开始
    start_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.System_Test_Ping_Start)))
    start_btn.click()
    time.sleep(20)  # 等待 Ping 完成

    # ========== 5. 检查结果：通过 page_source 全文搜索 ==========
    print(" 检查 Ping 结果...")
    page_source = driver.page_source

    # 匹配模式：64 bytes from [任意IP]: icmp_seq=... time=...
    pattern = r'64 bytes from \d+\.\d+\.\d+\.\d+: icmp_seq=\d+ ttl=\d+ time=\d+\.\d+ ms'

    if re.search(pattern, page_source):
        print("Ping www.jd.com 成功")
        print("\nPing 详细输出：")
        print("=" * 50)
        matches = re.findall(pattern, page_source)
        for match in matches:
            print(match)
        print("=" * 50)
    else:
        print("Ping www.jd.com 失败：未收到有效响应")
        assert False, "Ping www.jd.com 失败：未收到有效响应"


def handle_guide_wizard(driver):
    """处理重置后出现的向导界面，依次点击 Skip -> Skip -> Complete Setting"""
    wait = WebDriverWait(driver, 15)

    print("\n正在处理向导界面...")

    # ========== 第一步：密码设置页 -> 点击 Skip ==========
    try:
        skip_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.guide_skip)))
        skip_btn.click()
        print("已跳过密码设置")
    except Exception as e:
        print(f"跳过密码设置失败: {e}")

    # ========== 第二步：Wi-Fi 设置页 -> 点击 Skip ==========
    try:
        # 注意这里可能需要更精确的定位器来区分不同的“Skip”按钮
        skip_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.guide_skip)))
        skip_btn.click()
        print("已跳过 Wi-Fi 设置")
    except Exception as e:
        print(f"跳过 Wi-Fi 设置失败: {e}")
        # 尝试使用 Next


    # ========== 第三步：完成设置页 -> 点击 Complete Setting ==========
    try:
        complete_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.guide_complete)))
        complete_btn.click()
        print("已完成设置，进入主界面")
    except Exception as e:
        print(f"点击 Complete Setting 失败: {e}")
    time.sleep(5)


def save_screenshot_and_log(driver, name="screenshot"):
    """
    截图函数：
    - 根目录：D:\pytest_jenkins_test@tmp\photo_YYYY-MM-DD（按天）
    - 子目录：按调用脚本名（如 test_login.py → test-login）
    - 同一脚本多次调用：文件名自动编号（screenshot_00.png, _01.png...）
    """
    global _ROOT_DIR, _CREATED_SCRIPT_DIRS

    with _LOCK:
        # 1. 创建或复用当天的根目录（仅日期）
        if _ROOT_DIR is None:
            today = datetime.now().strftime("%Y-%m-%d")
            _ROOT_DIR = os.path.join(BASE_PARENT, f"photo_{today}")
            os.makedirs(_ROOT_DIR, exist_ok=True)
            print(f"使用截图根目录: {_ROOT_DIR}")

        # 2. 获取调用者脚本名
        frame = inspect.currentframe()
        try:
            caller_frame = frame.f_back
            if caller_frame is None:
                script_name = "unknown"
            else:
                caller_file = caller_frame.f_code.co_filename
                script_basename = os.path.basename(caller_file)
                script_name = script_basename.replace(".py", "").replace("_", "-").replace(".", "-")
        finally:
            del frame

        # 3. 构建子目录路径
        subdir_path = os.path.join(_ROOT_DIR, script_name)

        # 4. 如果该脚本子目录未创建，则创建
        if script_name not in _CREATED_SCRIPT_DIRS:
            os.makedirs(subdir_path, exist_ok=True)
            _CREATED_SCRIPT_DIRS.add(script_name)
            print(f"创建脚本子目录: {subdir_path}")

        # 5. 生成唯一文件名（自动编号）
        count = 0
        while True:
            filename = f"{name}_{count:02d}.png"
            filepath = os.path.join(subdir_path, filename)
            if not os.path.exists(filepath):
                break
            count += 1

        # 6. 执行截图
        try:
            driver.save_screenshot(filepath)
            print(f"截图已保存: {filepath}")
        except Exception as e:
            print(f"截图失败: {e}")
