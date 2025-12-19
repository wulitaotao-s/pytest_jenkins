import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import login, safe_set_input_value, restart_test_nic_and_ping
import element_config as ec


def test_wan_static_ping_jd(driver):
    """测试 WAN Static 模式 + Ping www.jd.com 连通性"""

    # ========== 1. 登录 ==========
    login(driver)

    # ========== 2. 进入 Basic > WAN 页面 ==========
    print("→ 跳转到 WAN 配置页面")
    driver.get(ec.Basic_wan)
    wait = WebDriverWait(driver, 15)

    # ========== 3. 配置 WAN 为 Static 模式 ==========
    print("→ 配置 WAN 为 Static 模式")

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

    # 设置 Connection Mode = Static
    conn_mode_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Connection_Mode)))
    conn_mode_input.click()
    static_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Connection_Mode_Static)))
    static_option.click()

    # 设置 IP Address
    print("→ 设置 IP 地址 = 192.168.100.200")
    safe_set_input_value(driver, ec.wan_IP_Address, "192.168.100.200")

    # 设置 Subnet Mask
    print("→ 设置子网掩码 = 255.255.255.0")
    safe_set_input_value(driver, ec.wan_Subnet_Mask, "255.255.255.0")

    # 设置 Default Gateway
    print("→ 设置默认网关 = 192.168.100.1")
    safe_set_input_value(driver, ec.wan_Default_Gateway, "192.168.100.1")

    # 设置 Primary DNS
    print("→ 设置主 DNS = 114.114.114.114")
    safe_set_input_value(driver, ec.wan_Primary_Dns, "114.114.114.114")

    # 设置 Secondary DNS
    print("→ 设置备用 DNS = 8.8.8.8")
    safe_set_input_value(driver, ec.wan_Secondary_Dns, "8.8.8.8")

    # 设置 VLAN ID = 100
    print("→ 设置 VLAN ID = 100")
    safe_set_input_value(driver, ec.wan_VLAN_ID, "100")

    # 设置 MTU = 1500
    print("→ 设置 MTU = 1500")
    safe_set_input_value(driver, ec.wan_MTU, "1500")

    # 启用 Nat Enable 开关
    switch = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_nat_enable)))
    if "t-is-checked" not in switch.get_attribute("class"):
        switch.click()
        print("→ 启用 Nat Enable")
    else:
        print("→ Nat Enable 已启用")

    # 启用 WAN 开关
    switch = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Enable)))
    if "t-is-checked" not in switch.get_attribute("class"):
        switch.click()
        print("→ 启用 WAN")
    else:
        print("→ WAN 已启用")

    # 保存配置
    print("→ 保存 WAN 配置")
    save_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_commit)))
    save_btn.click()
    time.sleep(10)  # 等待静态 IP 生效

    # ========== 4. 执行 Ping 测试 ==========
    print("→ 跳转到系统测试页面")
    driver.get(ec.Advanced_System_System_Test)
    wait = WebDriverWait(driver, 15)

    # 设置 Ping 次数
    safe_set_input_value(driver, ec.System_Test_Ping_Repeat_Times, "3")

    # 选择接口：Internet
    print("→ 选择 Ping 接口 = Internet")
    interface_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.System_Test_Ping_Interface)))
    interface_input.click()
    internet_opt = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.System_Test_Ping_INTERNET)))
    internet_opt.click()

    # 设置目标地址
    print("→ 设置 Ping 目标地址 = www.jd.com")
    safe_set_input_value(driver, ec.System_Test_Ping_Address, "www.jd.com")

    # 点击开始
    start_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.System_Test_Ping_Start)))
    start_btn.click()
    time.sleep(20)  # 等待 Ping 完成

    # ========== 5. 检查结果：通过 page_source 全文搜索 ==========
    print("→ 检查 Ping 结果...")
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

    # ========== 6. 检查下挂设备是否可访问互联网 ==========
    print("检查下挂设备是否可访问互联网...")
    if not restart_test_nic_and_ping():
        print("网卡重启或 Ping www.jd.com 失败，测试终止")
        assert False, "本地网络环境异常：Test 网卡无法正常通信"