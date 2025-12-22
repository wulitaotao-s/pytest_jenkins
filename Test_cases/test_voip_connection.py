import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import login, safe_set_input_value
import element_config as ec
import re


def test_voip_connection(driver):
    """测试 VoIP 连接配置：设置 VOICE WAN + VoIP 参数，验证注册状态和 Ping 诊断"""

    # ========== 1. 登录 ==========
    login(driver)

    # ========== 2. 进入 Basic > WAN 页面 ==========
    print("跳转到 WAN 配置页面")
    driver.get(ec.Basic_wan)
    wait = WebDriverWait(driver, 15)

    # ========== 3. 配置 VOICE WAN 条目 ==========
    # 点击 Request Name 输入框（展开下拉）
    print("点击 Request Name 下拉框")
    request_name_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Request_Name)))
    request_name_input.click()

    # 选择 VOICE 选项（精确匹配 title="3_VOICE_R_VID_300"）
    print("选择 Request Name = 3_VOICE_R_VID_300")
    voice_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Request_Name_VOICE)))
    voice_option.click()

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

    # 设置 VLAN ID = 300
    print("设置 VLAN ID = 300")
    safe_set_input_value(driver, ec.wan_VLAN_ID, "300")

    # 设置 MTU = 1500
    print("设置 MTU = 1500")
    safe_set_input_value(driver, ec.wan_MTU, "1500")

    # 启用 NAT Enable 开关
    nat_switch = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_nat_enable)))
    if "t-is-checked" not in nat_switch.get_attribute("class"):
        nat_switch.click()
        print("启用 NAT Enable")
    else:
        print("NAT Enable 已启用")

    # 启用 WAN 开关
    wan_switch = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_Enable)))
    if "t-is-checked" not in wan_switch.get_attribute("class"):
        wan_switch.click()
        print("启用 WAN")
    else:
        print("WAN 已启用")

    # 保存 WAN 配置
    print("保存 WAN 配置")
    save_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.wan_commit)))
    save_btn.click()
    time.sleep(3)

    # ========== 4. 配置 VoIP 设置 ==========
    print("跳转到 VoIP 配置页面")
    driver.get(ec.Basic_voip)

    # 设置 Binding Interface = 3_VOICE_R_VID_300
    print("设置 Protocol")
    binding_interface_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.voip_Protocol)))
    binding_interface_input.click()
    voice_interface_option = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.voip_Protocol_SIP)))
    voice_interface_option.click()

    # 设置 Register Server = 192.168.130.1:5060
    print("设置 Register Server = 192.168.130.1:5060")
    safe_set_input_value(driver, ec.voip_Register_Server, "192.168.130.1")
    safe_set_input_value(driver, ec.voip_Register_Server_port, "5060")

    # 设置 Proxy Server = 192.168.130.1:5060
    print("设置 Proxy Server = 192.168.130.1:5060")
    safe_set_input_value(driver, ec.voip_Proxy_Server, "192.168.130.1")
    safe_set_input_value(driver, ec.voip_Proxy_Server_port, "5060")

    # 设置 Outbound Proxy = 192.168.130.1:5060
    print("设置 Outbound Proxy = 192.168.130.1:5060")
    safe_set_input_value(driver, ec.voip_Outbound_Proxy, "192.168.130.1")
    safe_set_input_value(driver, ec.voip_Outbound_Proxy_port, "5060")

    # 设置 Secondary Register Server = 192.168.130.1:5060
    print("设置 Secondary Register Server = 192.168.130.1:5060")
    safe_set_input_value(driver, ec.voip_Secondary_Register_Server, "192.168.130.1")
    safe_set_input_value(driver, ec.voip_Secondary_Register_Server_port, "5060")

    # 设置 Secondary Proxy Server = 192.168.130.1:5060
    print("设置 Secondary Proxy Server = 192.168.130.1:5060")
    safe_set_input_value(driver, ec.voip_Secondary_Proxy_Server, "192.168.130.1")
    safe_set_input_value(driver, ec.voip_Secondary_Proxy_Server_port, "5060")

    # 设置 Secondary Outbound Proxy = 192.168.130.1:5060
    print("设置 Secondary Outbound Proxy = 192.168.130.1:5060")
    safe_set_input_value(driver, ec.voip_Secondary_Outbound_Proxy, "192.168.130.1")
    safe_set_input_value(driver, ec.voip_Secondary_Outbound_Proxy_port, "5060")

    # 设置 Account = 121212
    print("设置 Account = 121212")
    safe_set_input_value(driver, ec.voip_Account, "121212")

    # 设置 Password = 121212（假设为明文）
    print("设置 Password = 121212")
    safe_set_input_value(driver, ec.voip_Password, "121212")

    # 开启Port Enable
    wan_switch = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.voip_Port_Enable)))
    if "t-is-checked" not in wan_switch.get_attribute("class"):
        wan_switch.click()
        print("启用 WAN")
    else:
        print("WAN 已启用")

    # 保存 VoIP 配置
    print("保存 VoIP 配置")
    voip_save = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.voip_commit)))
    voip_save.click()
    time.sleep(20)  # 等待注册尝试完成

    # ========== 5. 验证 VoIP 注册状态 ==========
    print("检查 VoIP 注册状态")
    registration_status = driver.find_element(By.CSS_SELECTOR, ec.voip_Registration_Status).text
    if "Success" in registration_status or "Registered" in registration_status:
        print("VoIP 注册成功")
    else:
        print(f"VoIP 注册失败：{registration_status}")
        # assert False, f"VoIP 注册失败：{registration_status}"

    # ========== 6. 验证 语音 上报状态 ==========
    print("跳转到首页并进入 VOIP Information 页面")
    driver.get(ec.home)

    # 点击 Device 菜单
    print("点击 Device(1) 菜单")
    device_btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.DeviceName)))
    device_btn.click()
    time.sleep(1)

    # 点击 VOIP Information 子菜单
    print("点击 CWMP Information")
    cwmp_tab = wait.until(EC.element_to_be_clickable((By.XPATH, ec.VOIP_Information)))
    cwmp_tab.click()
    time.sleep(3)  # 等待页面加载和 ACS 上报完成

    # 检查页面是否包含 "Registered"
    print("检查是否显示 'Registered'")
    body_text = driver.find_element(By.TAG_NAME, "body").text
    if "Registered" in body_text:
        print("语音注册成功")
    else:
        print("未检测到 'Registered' 文本")
        # 可选：打印部分页面内容用于调试
        print("当前页面片段（前500字符）：")
        print(body_text[:500])
        assert False, "语音注册失败"

    # ========== 7. 执行 Ping 诊断 ==========
    print("执行 Ping 测试")
    driver.get(ec.Advanced_System_System_Test)

    # 设置 Ping 次数 = 3
    safe_set_input_value(driver, ec.System_Test_Ping_Repeat_Times, "3")

    # 选择接口：3_VOICE_R_VID_300
    print("选择 Ping 接口 = 3_VOICE_R_VID_300")
    interface_input = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.System_Test_Ping_Interface)))
    driver.execute_script("arguments[0].click();", interface_input)
    target_interface = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ec.System_Test_Ping_VOICE)))
    target_interface.click()

    # 设置目标地址
    print("设置 Ping 目标地址")
    safe_set_input_value(driver, ec.System_Test_Ping_Address, "192.168.130.1")

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
    target_ip = "192.168.130.1"
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