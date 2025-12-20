import os
import sys
import subprocess
import re
from datetime import datetime

WORKSPACE = os.getenv("WORKSPACE", ".")
REPORT_DIR = os.path.join(WORKSPACE, "report")
os.makedirs(REPORT_DIR, exist_ok=True)

LOG_FILE = os.path.join(REPORT_DIR, "test_run.log")

with open(LOG_FILE, "w", encoding="utf-8") as f:
    def log(msg):
        print(msg)
        f.write(msg + "\n")
        f.flush()

    log("测试开始")
    start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log(f"测试开始时间: {start_time}")

    device_type = "FT-35"
    software_version = "V1.0.13"
    log(f"Device Type: {device_type}, Software Version: {software_version}")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    detailed_log_path = f"D:\\pytest_jenkins\\Reports\\{timestamp} {device_type} {software_version}.log"
    os.makedirs(os.path.dirname(detailed_log_path), exist_ok=True)

    try:
        result = subprocess.run([
            sys.executable, "-m", "pytest",
            "test_acs_connection.py",
            "--tb=short",
            "-v"
        ], capture_output=True, text=True, cwd=os.getcwd())

        with open(detailed_log_path, "w", encoding="utf-8") as detail_f:
            detail_f.write(result.stdout)
            if result.stderr:
                detail_f.write("\n[STDERR]\n" + result.stderr)

        log(f"Log saved to: {detailed_log_path}")

        # 正确提取通过/失败数
        passed = len(re.findall(r"PASSED", result.stdout))
        failed = len(re.findall(r"FAILED", result.stdout))

        log(f"Summary: {passed} passed, {failed} failed")

    except Exception as e:
        log(f"Error running tests: {e}")
        log("Summary: 0 passed, 1 failed")

    end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log(f"测试结束时间: {end_time}")
    log("测试结束")

# 设置环境变量供 send_email.py 使用
os.environ["DETAILED_LOG_PATH"] = detailed_log_path