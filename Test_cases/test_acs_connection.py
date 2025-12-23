import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import login, safe_set_input_value
import element_config as ec
import re

def test_acs_connection(driver):
    """测试 ACS 连接配置：设置 TR069 WAN + CWMP，验证连通性"""

    # ========== 1. 登录 ==========
    login(driver)

    # ========== 2. 进入 Basic > WAN 页面 ==========
    print("跳转到 WAN 配置页面")
    driver.get(ec.Basic_wan)
    wait = WebDriverWait(driver, 15)

    # ========== 3. 配置 TR069 WAN 条目 ==========
    # 点击 Request Name 输入框（展开下拉）
    print("点击 Request Name 下拉框")
    request_name_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Request_Name)))
    request_name_input.click()

    # 选择 TR069 选项（精确匹配 title="TR069"）
    print("选择 Request Name = TR069")
    tr069_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Request_Name_TR069)))
    tr069_option.click()

    # 设置 Access Type = Route
    print("设置 Access Type = Route")
    access_type_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Access_Type)))
    access_type_input.click()
    route_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Access_Type_Route)))
    route_option.click()

    # 设置 Bearer Service = TR069
    print("设置 Bearer Service = TR069")
    bearer_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Bearer_Service)))
    bearer_input.click()
    bearer_tr069 = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Bearer_Service_TR069)))
    bearer_tr069.click()

    # 设置 Connection Mode = DHCP（仅在 Route 模式下出现）
    print("设置 Connection Mode = DHCP")
    conn_mode_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Connection_Mode)))
    conn_mode_input.click()
    dhcp_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Connection_Mode_DHCP)))
    dhcp_option.click()

    # 设置 VLAN ID = 400（使用 JS 安全设置）
    print("设置 VLAN ID = 400")
    safe_set_input_value(driver, ec.wan_VLAN_ID, "400")

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

    # ========== 4. 配置 CWMP ==========
    print("跳转到 CWMP 配置页面")
    driver.get(ec.Basic_cwmp)

    # 启用 Periodic Notification（可选）
    period_enable = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.cwmp_Periodic_Notification_Enable)))
    if not period_enable.is_selected():
        period_enable.click()

    # 设置 Interval = 30
    print("设置 Notification Interval = 30")
    safe_set_input_value(driver, ec.cwmp_Notification_Interval, "30")

    # 设置 ACS Server URL
    print("设置 ACS Server URL")
    safe_set_input_value(driver, ec.cwmp_Server_URL, "http://192.168.140.2:7547")

    # 设置 Platform 用户名/密码
    print("设置 Platform 认证信息")
    safe_set_input_value(driver, ec.cwmp_Platform_Username, "admin")
    safe_set_input_value(driver, ec.cwmp_Platform_Password, "admin")

    # 设置 Terminal 用户名/密码
    print("设置 Terminal 认证信息")
    safe_set_input_value(driver, ec.cwmp_Terminal_Username, "admin")
    safe_set_input_value(driver, ec.cwmp_Terminal_Password, "admin")

    # 保存 CWMP 配置
    print("保存 CWMP 配置")
    cwmp_save = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.cwmp_commit)))
    cwmp_save.click()
    time.sleep(5)  # 等待 ACS 连接建立

    # ========== 5. 验证连接状态 ==========
    print("返回 WAN 页面检查 TR069 连接状态")
    driver.get(ec.Basic_wan)
    time.sleep(10)

    page_text = driver.find_element(By.TAG_NAME, "body").text
    connected = "Connected" in page_text
    if connected:
        print("TR069 WAN 已成功连接")
    else:
        print("TR069 WAN 未连接")

    # ========== 6. 验证 CWMP 上报状态 ==========
    print("跳转到首页并进入 CWMP Information 页面")
    driver.get(ec.home)

    # 点击 Device(1) 菜单
    print("点击 Device(1) 菜单")
    device_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.DeviceName)))
    device_btn.click()
    time.sleep(1)

    # 点击 CWMP Information 子菜单
    print("点击 CWMP Information")
    cwmp_tab = wait.until(EC.element_to_be_clickable((By.XPATH, ec.CWMP_Information)))
    cwmp_tab.click()
    time.sleep(3)  # 等待页面加载和 ACS 上报完成

    # 检查页面是否包含 "Reported successfully"
    print("检查是否显示 'Reported successfully'")
    body_text = driver.find_element(By.TAG_NAME, "body").text
    if "Reported successfully" in body_text:
        print("CWMP 已上报成功")
    else:
        print("未检测到 'Reported successfully' 文本")

    # ========== 7. Ping 测试 ==========
    print("执行 Ping 测试")
    driver.get(ec.Advanced_System_System_Test)

    # 设置 Ping 次数
    safe_set_input_value(driver, ec.System_Test_Ping_Repeat_Times, "3")

    # 选择接口（TR069）
    interface_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.System_Test_Ping_Interface)))
    driver.execute_script("arguments[0].click();", interface_input)
    internet_opt = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.System_Test_Ping_Interface_TR069)))
    internet_opt.click()

    # 设置目标地址
    print("设置 Ping 目标地址")
    safe_set_input_value(driver, ec.System_Test_Ping_Address, "192.168.140.1")

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
    target_ip = "192.168.140.1"
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