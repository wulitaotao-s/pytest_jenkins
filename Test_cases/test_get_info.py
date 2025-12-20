# Test_cases/test_get_info.py
from conftest import login
import re


def test_extract_device_info(driver):
    """从页面全文本中提取 Device Type 和 Software Version"""

    # 1. 登录
    login(driver)

    # 2. 获取整个页面的可见文本
    page_text = driver.find_element("tag name", "body").text

    # 3. 打印调试（可选）
    print("=== 全文内容 ===")
    print(page_text)

    # 4. 使用正确正则：匹配 "Device Type XXX" 在同一行
    device_type_match = re.search(r"Device\s+Type\s+([A-Z0-9-]+)", page_text)
    software_version_match = re.search(r"Software\s+Version\s+([A-Z0-9.]+)", page_text)

    device_type = device_type_match.group(1) if device_type_match else "Unknown"
    software_version = software_version_match.group(1) if software_version_match else "Unknown"

    # 5. 打印（关键！供 run_all_tests.py 捕获）
    print(f"Device Type: {device_type}")
    print(f"Software Version: {software_version}")

    # 6. 验证
    assert device_type != "Unknown", "Failed to extract Device Type"
    assert software_version != "Unknown", "Failed to extract Software Version"