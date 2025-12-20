# run_all_tests.py
import os
import sys
import subprocess
import datetime
from pathlib import Path

# === 配置路径 ===
BASE_DIR = Path(__file__).parent.resolve()
TEST_DIR = BASE_DIR / "Test_cases"
REPORTS_DIR = BASE_DIR / "Reports"
REPORTS_DIR.mkdir(exist_ok=True)

# === 全局变量：用于传递设备信息 ===
DEVICE_TYPE = "UnknownDevice"
SOFTWARE_VERSION = "UnknownVersion"


def sanitize_filename_part(s: str) -> str:
    """清理字符串，使其可作为文件名的一部分"""
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in s)


def extract_device_info_from_output(output: str):
    """从 pytest 输出中提取设备型号和软件版本"""
    global DEVICE_TYPE, SOFTWARE_VERSION
    for line in output.splitlines():
        if "Device Type:" in line:
            value = line.split("Device Type:", 1)[-1].strip()
            if value and value != "Unknown":
                DEVICE_TYPE = value
        if "Software Version:" in line:
            value = line.split("Software Version:", 1)[-1].strip()
            if value and value != "Unknown":
                SOFTWARE_VERSION = value


def get_test_files_in_order():
    """返回测试文件列表，确保 test_get_info.py 第一个"""
    all_files = [f for f in os.listdir(TEST_DIR) if f.startswith("test_") and f.endswith(".py")]
    ordered = []
    others = []
    for f in all_files:
        if f == "test_get_info.py":
            ordered.append(f)
        else:
            others.append(f)
    others.sort()
    return ordered + others


def main():
    global DEVICE_TYPE, SOFTWARE_VERSION
    start_time = datetime.datetime.now()
    timestamp_for_logname = start_time.strftime('%Y-%m-%d_%H-%M-%S')

    test_files = get_test_files_in_order()
    if not test_files:
        print("No test files found in Test_cases/")
        return

    # 确保第一个是 test_get_info.py
    if test_files[0] != "test_get_info.py":
        print("ERROR: test_get_info.py must be the first test file!")
        sys.exit(1)

    all_outputs = []
    total_passed = 0
    total_failed = 0

    # === Step 1: 先运行 test_get_info.py 单独提取设备信息 ===
    first_file = test_files[0]
    print(f">>> Running device info extraction: {first_file}")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-v", "-s", str(TEST_DIR / first_file)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace"
    )
    output = result.stdout + result.stderr
    all_outputs.append((first_file, result.returncode, output))

    # 提取设备信息
    extract_device_info_from_output(output)
    print(f"INFO: Extracted device info -> Type: {DEVICE_TYPE}, Version: {SOFTWARE_VERSION}")

    # 统计结果
    if result.returncode == 0:
        total_passed += 1
    else:
        total_failed += 1

    # === Step 2: 运行其余测试 ===
    for filename in test_files[1:]:
        print(f">>> Running test: {filename}")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-v", "-s", str(TEST_DIR / filename)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        output = result.stdout + result.stderr
        all_outputs.append((filename, result.returncode, output))
        if result.returncode == 0:
            total_passed += 1
        else:
            total_failed += 1

    # === Step 3: 生成日志文件名（现在已有设备信息！）===
    safe_device = sanitize_filename_part(DEVICE_TYPE)
    safe_version = sanitize_filename_part(SOFTWARE_VERSION)
    log_filename = f"{timestamp_for_logname} {safe_device} {safe_version}.log"
    log_path = REPORTS_DIR / log_filename

    # 写入完整日志
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"Test Run Summary\n")
        f.write(f"Start Time: {start_time}\n")
        f.write(f"Device Type: {DEVICE_TYPE}\n")
        f.write(f"Software Version: {SOFTWARE_VERSION}\n")
        f.write(f"Total Tests: {len(test_files)} | Passed: {total_passed} | Failed: {total_failed}\n")
        f.write("=" * 80 + "\n\n")

        for filename, returncode, output in all_outputs:
            status = "PASSED" if returncode == 0 else "FAILED"
            f.write(f"[{status}] {filename}\n")
            f.write("-" * 60 + "\n")
            f.write(output)
            f.write("\n" + "=" * 80 + "\n\n")

    print(f"\n✅ All tests completed.")
    print(f"Log saved to: {log_path}")
    print(f"Summary: {total_passed} passed, {total_failed} failed")

    # === Step 4: 发送邮件（传入日志路径）===
    try:
        from send_email import send_test_report_email
        send_test_report_email(str(log_path))
    except Exception as e:
        print(f"WARNING: Failed to send email: {e}")


if __name__ == "__main__":
    main()