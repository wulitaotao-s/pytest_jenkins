import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import login, safe_set_input_value, restart_test_nic_and_ping, save_screenshot_and_log
import element_config as ec


def test_wan_pppoe_ping_jd(driver):
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
    save_screenshot_and_log(driver)

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
    save_screenshot_and_log(driver)

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

    # ========== 6. 检查下挂设备是否可访问互联网 ==========
    print("检查下挂设备是否可访问互联网...")
    if not restart_test_nic_and_ping():
        print("网卡重启或 Ping www.jd.com 失败，测试终止")
        assert False, "本地网络环境异常：Test 网卡无法正常通信"