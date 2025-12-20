# run_all_tests.py
import os
import sys
import subprocess
import datetime
from pathlib import Path

# 固定报告目录（绝对路径）
REPORTS_DIR = Path("D:/pytest_jenkins/Reports")
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# 全局设备信息
DEVICE_TYPE = "UnknownDevice"
SOFTWARE_VERSION = "UnknownVersion"


def sanitize_filename_part(s):
    return "".join(c if c.isalnum() or c in "._-" else "_" for c in s)


def extract_device_info_from_output(output):
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
    test_dir = Path("Test_cases")
    all_files = [f for f in os.listdir(test_dir) if f.startswith("test_") and f.endswith(".py")]
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
        print("No test files found.")
        return

    if test_files[0] != "test_get_info.py":
        print("Error: test_get_info.py must be first.")
        sys.exit(1)

    all_outputs = []
    total_passed = 0
    total_failed = 0

    # Step 1: Run test_get_info.py first
    first_file = test_files[0]
    test_path = Path("Test_cases") / first_file
    print(f"Running device info extraction: {first_file}")

    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"

    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-v", "-s", str(test_path)],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        env=env
    )
    output = result.stdout + result.stderr
    all_outputs.append((first_file, result.returncode, output))
    extract_device_info_from_output(output)
    print(f"Device Type: {DEVICE_TYPE}, Software Version: {SOFTWARE_VERSION}")

    if result.returncode == 0:
        total_passed += 1
    else:
        total_failed += 1

    # Step 2: Run other tests
    for filename in test_files[1:]:
        test_path = Path("Test_cases") / filename
        print(f"Running test: {filename}")
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-v", "-s", str(test_path)],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env
        )
        output = result.stdout + result.stderr
        all_outputs.append((filename, result.returncode, output))
        if result.returncode == 0:
            total_passed += 1
        else:
            total_failed += 1

    # Step 3: Generate log file with device info
    safe_device = sanitize_filename_part(DEVICE_TYPE)
    safe_version = sanitize_filename_part(SOFTWARE_VERSION)
    log_filename = f"{timestamp_for_logname} {safe_device} {safe_version}.log"
    log_path = REPORTS_DIR / log_filename

    # Write log in UTF-8
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("Test Run Summary\n")
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

    print(f"Log saved to: {log_path}")
    print(f"Summary: {total_passed} passed, {total_failed} failed")

    # Step 4: Send email
    try:
        from send_email import send_test_report_email
        send_test_report_email(str(log_path))
    except Exception as e:
        print(f"Failed to send email: {e}")


if __name__ == "__main__":
    main()