import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from element_config import *
from conftest import login


@pytest.mark.usefixtures("driver")
def test_acs_connection(driver):
    """测试 ACS 服务器连接配置并验证连接状态"""

    print("→ 执行登录操作")
    login(driver)
    print("→ 登录完成")

    # 进入 Basic > WAN 页面
    print("→ 跳转到 WAN 配置页面")
    driver.get(basic_wan_page)
    print("→ 已进入 WAN 页面")

    # 设置 Request Name 为 TR069
    print("→ 点击 Request Name 下拉框")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, wan_service_name_field))
    ).click()
    print("→ Request Name 下拉框已展开")

    print("→ 选择 Request Name = TR069")
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, wan_service_name_option_TR069))
    ).click()
    print("→ Request Name 设置为 TR069")

    # 设置 Access Type 为 Route
    print("→ 点击 Access Type (Work Mode) 下拉框")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, wan_work_mode_field))
    ).click()
    print("→ Access Type 下拉框已展开")

    print("→ 选择 Access Type = Route")
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, wan_work_mode_option_Route))
    ).click()
    print("→ Access Type 设置为 Route")

    # 设置 Bearer Service 为 TR069
    print("→ 点击 Bearer Service 下拉框")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, wan_bearer_service_field))
    ).click()
    print("→ Bearer Service 下拉框已展开")

    print("→ 选择 Bearer Service = TR069")
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, wan_bearer_service_option_TR069))
    ).click()
    print("→ Bearer Service 设置为 TR069")

    # 设置 Connection Mode 为 DHCP
    print("→ 点击 Connection Mode 下拉框")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, wan_conn_mode_field))
    ).click()
    print("→ Connection Mode 下拉框已展开")

    print("→ 选择 Connection Mode = DHCP")
    WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, wan_conn_mode_option_DHCP))
    ).click()
    print("→ Connection Mode 设置为 DHCP")

    # 设置 VLAN ID = 400
    print("→ 设置 VLAN ID = 400")
    vlan_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, wan_vlan_id_field))
    )
    driver.execute_script("arguments[0].value = '400';", vlan_input)
    print("→ VLAN ID 已设置为 400")

    # 设置 MTU = 1500
    print("→ 设置 MTU = 1500")
    mtu_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, wan_mtu_field))
    )
    driver.execute_script("arguments[0].value = '1500';", mtu_input)
    print("→ MTU 已设置为 1500")

    # 保存 WAN 配置
    print("→ 点击保存按钮（WAN 配置）")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, wan_save_button))
    ).click()
    print("→ WAN 配置已保存")

    # 进入 Basic > CWMP 页面
    print("→ 跳转到 CWMP 配置页面")
    driver.get(basic_cwmp_page)
    print("→ 已进入 CWMP 页面")

    # 填写 Server URL
    print("→ 设置 ACS Server URL")
    acs_url = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, cwmp_acs_url_field))
    )
    driver.execute_script("arguments[0].value = 'http://192.168.140.2:7547';", acs_url)
    print("→ ACS Server URL 已设置")

    # 填写 Platform Username / Password
    print("→ 设置 Platform Username")
    acs_user = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, cwmp_acs_username_field))
    )
    driver.execute_script("arguments[0].value = 'admin';", acs_user)
    print("→ Platform Username 已设置")

    print("→ 设置 Platform Password")
    acs_pass = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, cwmp_acs_password_field))
    )
    driver.execute_script("arguments[0].value = 'admin';", acs_pass)
    print("→ Platform Password 已设置")

    # 填写 Terminal Username / Password
    print("→ 设置 Terminal Username")
    client_user = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, cwmp_client_username_field))
    )
    driver.execute_script("arguments[0].value = 'admin';", client_user)
    print("→ Terminal Username 已设置")

    print("→ 设置 Terminal Password")
    client_pass = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, cwmp_client_password_field))
    )
    driver.execute_script("arguments[0].value = 'admin';", client_pass)
    print("→ Terminal Password 已设置")

    # 保存 CWMP 配置
    print("→ 点击保存按钮（CWMP 配置）")
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, cwmp_save_button))
    ).click()
    print("→ CWMP 配置已保存")

    # 等待 15 秒让连接建立
    print("→ 等待 15 秒以建立 ACS 连接...")
    time.sleep(15)
    print("→ 等待完成")

    # 返回 WAN 页面检查 Connection Status
    print("→ 返回 WAN 页面检查连接状态")
    driver.get(basic_wan_page)
    status_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, wan_connection_status))
    )
    actual_status = status_element.text.strip()
    print(f"→ 当前 Connection Status: '{actual_status}'")

    print("进入 Advanced > System > System Test 页面")
    driver.get(advanced_system_test_page)
    print("已进入 Ping Test 页面")

    print("设置 Repeat Times = 3")
    repeat_times_select = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ping_repeat_times_field))
    )
    driver.execute_script("arguments[0].value = '3';", repeat_times_select)
    print("Repeat Times 设置为 3")

    print("设置 Interface = 1_TR069_R_VID_400")
    interface_select = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ping_interface_field))
    )
    driver.execute_script("arguments[0].value = '1_TR069_R_VID_400';", interface_select)
    print("Interface 设置为 1_TR069_R_VID_400")

    print("设置 Address = 192.168.140.1")
    address_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ping_address_field))
    )
    driver.execute_script("arguments[0].value = '192.168.140.1';", address_input)
    print("Address 设置为 192.168.140.1")

    print("点击 Start 按钮执行 Ping")
    start_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ping_start_button))
    )
    start_button.click()
    print("Ping 已启动")

    print("等待 Ping 结果返回...")
    time.sleep(5)

    # 检查是否出现成功提示
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ping_result_success))
        )
        print("Ping 成功提示已出现")
    except:
        raise AssertionError("Ping 测试失败：未检测到成功提示")

    # 获取详细结果文本
    result_text_element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ping_result_text))
    )
    result_text = result_text_element.text.strip()
    print("Ping 详细结果：")
    print(result_text)

    # 验证结果中包含响应时间
    if "time=" not in result_text:
        raise AssertionError("Ping 结果无效：未包含响应时间（可能超时或未发送）")

    print("Ping 诊断测试通过：192.168.140.1 可达")



    assert actual_status == "Connected", f"期望状态为 'Connected'，实际为 '{actual_status}'"
    print(" ACS 连接验证通过")