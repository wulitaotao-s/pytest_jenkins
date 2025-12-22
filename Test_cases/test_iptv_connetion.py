import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import login, safe_set_input_value
import element_config as ec
import re


def test_wan_iptv_ping_diagnosis(driver):
    """测试 WAN + IPTV 配置及 Ping 诊断：设置 WAN VLAN=200, IPTV Multicast VLAN=3030，执行 Ping 测试"""

    # ========== 1. 登录 ==========
    login(driver)

    # ========== 2. 进入 Basic > WAN 页面 ==========
    print("跳转到 WAN 配置页面")
    driver.get(ec.Basic_wan)
    wait = WebDriverWait(driver, 15)

    # ========== 3. 配置 WAN 条目 ==========
    # 点击 Request Name 输入框（展开下拉）
    print("点击 Request Name 下拉框")
    request_name_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Request_Name)))
    request_name_input.click()

    # 选择 Other 选项（精确匹配 title="TR069"）
    print("选择 Request Name = TR069")
    tr069_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Request_Name_OTHER)))
    tr069_option.click()

    # 设置 Access Type = Route
    print("设置 Access Type = Route")
    access_type_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Access_Type)))
    access_type_input.click()
    route_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Access_Type_Route)))
    route_option.click()

    # 设置 Connection Mode = DHCP
    print("设置 Connection Mode = DHCP")
    conn_mode_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Connection_Mode)))
    conn_mode_input.click()
    dhcp_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Connection_Mode_DHCP)))
    dhcp_option.click()

    # 设置 VLAN ID = 200
    print("设置 VLAN ID = 200")
    safe_set_input_value(driver, ec.wan_VLAN_ID, "200")

    # 设置 MTU = 1500
    print("设置 MTU = 1500")
    safe_set_input_value(driver, ec.wan_MTU, "1500")

    # 启用 Nat Enable 开关
    switch = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_nat_enable)))
    if "t-is-checked" not in switch.get_attribute("class"):
        switch.click()
        print("启用 Nat Enable")
    else:
        print("Nat Enable 已启用")

    # 启用 WAN 开关
    switch = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Enable)))
    if "t-is-checked" not in switch.get_attribute("class"):
        switch.click()
        print("启用 WAN")
    else:
        print("WAN 已启用")

    # 保存 WAN 配置
    print("保存 WAN 配置")
    save_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_commit)))
    save_btn.click()
    time.sleep(3)

    # ========== 4. 配置 IPTV ==========
    print("跳转到 IPTV 配置页面")
    driver.get(ec.Basic_iptv)

    # 设置 Multicast VLAN ID = 3030
    print("设置 Multicast VLAN ID = 3030")
    safe_set_input_value(driver, ec.iptv_Multicast_VLAN_ID, "3030")

    # 保存 IPTV 配置
    print("保存 IPTV 配置")
    iptv_save = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.iptv_commit)))
    iptv_save.click()
    time.sleep(3)

    # ========== 5. 执行 Ping 诊断 ==========
    print("执行 Ping 测试")
    driver.get(ec.Advanced_System_System_Test)

    # 设置 Ping 次数 = 3
    safe_set_input_value(driver, ec.System_Test_Ping_Repeat_Times, "3")

    # 选择接口：4_OTHER_R_VID_200
    print("选择 Ping 接口 = 4_OTHER_R_VID_200")
    interface_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.System_Test_Ping_Interface)))
    driver.execute_script("arguments[0].click();", interface_input)
    target_interface = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.System_Test_Ping_OTHER)))
    target_interface.click()

    # 设置目标地址
    print("设置 Ping 目标地址")
    safe_set_input_value(driver, ec.System_Test_Ping_Address, "192.168.120.1")

    # 开始 Ping
    start_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.System_Test_Ping_Start)))
    start_btn.click()
    time.sleep(5)

    # 等待 Ping 完成（最多 10 秒）
    wait = WebDriverWait(driver, 10)
    ping_logs_elem = wait.until(EC.presence_of_element_located((By.ID, "pingLogs")))

    # 获取整个页面源码
    page_source = driver.page_source

    # 目标 IP 和匹配模式
    target_ip = "192.168.120.1"
    pattern = rf'64 bytes from {target_ip}: icmp_seq=\d+ ttl=\d+ time=\d+\.\d+ ms'

    # 搜索是否包含成功响应
    if re.search(pattern, page_source):
        print("Ping 测试通过")
        print("\nPing 详细输出：")
        print("=" * 50)
        matches = re.findall(pattern, page_source)
        for match in matches:
            print(match)
        print("=" * 50)
    else:
        print(f"Ping 测试失败：未找到来自 {target_ip} 的有效响应")
        assert False, f"Ping 测试失败：未找到来自 {target_ip} 的有效响应"