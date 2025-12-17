# Test_cases/test_device_info.py

import pytest
from datetime import datetime
from io import StringIO
from selenium.webdriver.common.by import By
from conftest import login, save_test_log


class DeviceInfoTest:
    def __init__(self, driver):
        self.driver = driver
        self.log_buffer = StringIO()

    def _log(self, message):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        line = f"[{timestamp}] {message}"
        print(line)
        self.log_buffer.write(line + "\n")

    def run(self):
        try:
            self._log("开始测试：仅读取 Device Information")
            login(self.driver)

            self._log("正在提取 Device Information 表格数据...")

            # 直接查找页面中所有表格行（不依赖 .t-table）
            rows = self.driver.find_elements(By.CSS_SELECTOR, "table tbody tr")
            device_info = {}

            for row in rows:
                tds = row.find_elements(By.TAG_NAME, "td")
                if len(tds) >= 2:
                    key = tds[0].text.strip()
                    value = tds[1].text.strip()
                    if key and value not in ["-", "N/A", ""]:
                        device_info[key] = value

            # 直接打印字典（最简单方式）
            print("\n提取到的 Device Information:")
            print(device_info)

            self._log("测试完成")

        except Exception as e:
            error_msg = f"测试异常: {e}"
            self._log(error_msg)
            raise

        finally:
            save_test_log(self.log_buffer.getvalue())


def test_device_info_only(driver):
    tester = DeviceInfoTest(driver)
    tester.run()