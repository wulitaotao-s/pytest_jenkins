# test_device_info.py
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from conftest import login

@pytest.mark.usefixtures("driver")
def test_device_information_direct(driver):
    """测试登录后首页的 Device Information 表格"""
    print("🚀 开始测试首页 Device Information")

    # 1. 登录
    login(driver)

    # 2. 直接访问首页（无需点击）
    print("✅ 已进入首页")

    # 3. 等待 Device Information 表格加载
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Device Type')]"))
    )
    print("✅ Device 信息区域已加载")

    # 4. 获取所有表格行
    table_rows = driver.find_elements(By.XPATH, "//table//tr")

    # 5. 遍历每一行，提取 key-value
    for row in table_rows:
        cells = row.find_elements(By.TAG_NAME, "td")
        if len(cells) == 2:
            key = cells[0].text.strip()
            value = cells[1].text.strip()
            print(f"{key}: {value}")

    print("✅ 测试完成！")