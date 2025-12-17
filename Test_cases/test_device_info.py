# Test_cases/test_device_info.py

import pytest
import time
from datetime import datetime
from io import StringIO
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from conftest import login, save_test_log
import element_config as ec


class DevicePonInfoTest:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.step_count = 0
        self.total_steps = 4

    def _log(self, message, status="🔹"):
        self.step_count += 1
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] [STEP {self.step_count}/{self.total_steps}] {status} {message}")

    def _click_menu_item(self, text):
        locators = [
            (By.XPATH, f"//*[contains(text(), '{text}') and not(ancestor::*[contains(@style, 'display:none') or contains(@style, 'visibility:hidden')])]"),
            (By.XPATH, f"//button[contains(., '{text}')]"),
            (By.XPATH, f"//div[contains(., '{text}')]"),
            (By.XPATH, f"//span[contains(., '{text}')]"),
        ]
        for by, value in locators:
            try:
                element = self.wait.until(EC.element_to_be_clickable((by, value)))
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
                element.click()
                return True
            except Exception:
                continue
        return False

    def _extract_table_data(self):
        data = {}
        rows = self.driver.find_elements(By.CSS_SELECTOR, ".t-table tbody tr")
        for row in rows:
            tds = row.find_elements(By.TAG_NAME, "td")
            if len(tds) == 2:
                key = tds[0].text.strip()
                value = tds[1].text.strip()
                if key and value not in ["-", "N/A"]:
                    data[key] = value
        return data

    def _format_table(self, data, title):
        lines = [f"\n🔍 {title}:"]
        items = list(data.items())
        for i, (key, val) in enumerate(items):
            prefix = "└── " if i == len(items) - 1 else "├── "
            lines.append(f"{prefix}{key}: {val}")
        return "\n".join(lines)

    def run(self):
        # 捕获所有 print 输出
        old_stdout = sys.stdout
        log_buffer = StringIO()
        sys.stdout = log_buffer

        try:
            self._log("登录设备...")
            login(self.driver)

            # Device Info
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".t-table tbody tr")))
            device_info = self._extract_table_data()
            self._log("成功加载 Device Information 页面", "✅")

            # PON Info
            self._log("正在尝试进入 PON Information 页面...")
            if not self._click_menu_item("PON Information"):
                raise RuntimeError("无法点击 'PON Information' 菜单项")
            self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".t-table tbody tr")))
            pon_info = self._extract_table_data()
            self._log("成功进入 PON Information 页面", "✅")

            # 输出结果
            self._log("提取并验证关键字段...", "🔍")
            print(self._format_table(device_info, "Device Information"))
            print(self._format_table(pon_info, "PON Information"))
            print("\n✅ 所有关键字段均已验证！")

            # 验证关键字段
            all_info = {**device_info, **pon_info}
            required = ["Transmiting Light Power", "Receiving Light Power"]
            missing = [f for f in required if f not in all_info]
            if missing:
                pytest.fail(f"缺失关键字段: {missing}")

        finally:
            # 恢复 stdout 并保存日志
            sys.stdout = old_stdout
            content = log_buffer.getvalue()
            save_test_log(content)


def test_device_and_pon_info(driver):
    tester = DevicePonInfoTest(driver)
    tester.run()