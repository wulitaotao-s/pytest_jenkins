# run_all_tests.py
import subprocess
import sys
import os
import re
from datetime import datetime

# === 配置 ===
BASE_REPORT_DIR = r"D:\pytest_jenkins\report"
os.makedirs(BASE_REPORT_DIR, exist_ok=True)

TEST_DIR = "Test_cases"

# 默认值
DEVICE_TYPE = "UnknownDevice"
SOFTWARE_VERSION = "UnknownVersion"


def extract_device_info_from_output(output: str):
    """从输出中提取 Device Type 和 Software Version"""
    global DEVICE_TYPE, SOFTWARE_VERSION
    lines = output.splitlines()
    for line in lines:
        if "Device Type:" in line:
            try:
                DEVICE_TYPE = line.split("Device Type:")[-1].strip() or DEVICE_TYPE
            except:
                pass
        if "Software Version:" in line:
            try:
                SOFTWARE_VERSION = line.split("Software Version:")[-1].strip() or SOFTWARE_VERSION
            except:
                pass


def get_test_files_in_order():
    """返回测试文件列表，确保 test_a_device_info.py 第一个"""
    all_files = []
    if not os.path.exists(TEST_DIR):
        print(f"错误：目录 {TEST_DIR} 不存在")
        return []

    # 收集所有 test_*.py 文件
    for f in os.listdir(TEST_DIR):
        if f.startswith("test_") and f.endswith(".py"):
            all_files.append(f)

    # 确保 test_a_device_info.py 在最前面
    ordered = []
    other_files = []

    for f in all_files:
        if f == "test_get_info.py":
            ordered.append(f)
        else:
            other_files.append(f)

    # 排序其他文件（可选）
    other_files.sort()
    ordered.extend(other_files)

    return ordered


def sanitize_filename_part(s: str) -> str:
    """清理字符串，使其可作为文件名"""
    return "".join(c if c.isalnum() or c in (" ", ".", "-", "_") else "_" for c in s)


def main():
    global DEVICE_TYPE, SOFTWARE_VERSION

    start_time = datetime.now()
    timestamp_for_logname = start_time.strftime('%Y-%m-%d_%H-%M-%S')

    test_files = get_test_files_in_order()

    if not test_files:
        print("未找到任何测试文件！")
        sys.exit(1)

    print(f"发现 {len(test_files)} 个测试文件，按顺序执行：")
    for i, f in enumerate(test_files, 1):
        print(f"  {i}. {f}")

    # 存储每个文件的输出和结果
    all_outputs = []
    total_passed = 0
    total_failed = 0

    # 逐个运行测试文件
    for idx, filename in enumerate(test_files):
        filepath = os.path.join(TEST_DIR, filename)
        print(f"\n>>> 正在执行 [{idx+1}/{len(test_files)}]: {filename}")

        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-v", "-s", filepath],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        output = result.stdout + result.stderr
        all_outputs.append((filename, result.returncode, output))

        # 如果是第一个文件，尝试提取设备信息
        if idx == 0:
            extract_device_info_from_output(output)

    # 构建唯一日志文件名（带精确时间戳）
    safe_device = sanitize_filename_part(DEVICE_TYPE)
    safe_version = sanitize_filename_part(SOFTWARE_VERSION)
    log_filename = f"{timestamp_for_logname} {safe_device} {safe_version}.log"
    log_path = os.path.join(BASE_REPORT_DIR, log_filename)

    # 写入日志
    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"测试开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"设备型号: {DEVICE_TYPE}\n")
        f.write(f"软件版本: {SOFTWARE_VERSION}\n")
        f.write("=" * 80 + "\n\n")

        for filename, returncode, output in all_outputs:
            status = "PASS" if returncode == 0 else "FAIL"
            if returncode == 0:
                total_passed += 1
            else:
                total_failed += 1

            f.write("\n\n")
            f.write("=" * 80 + "\n")
            f.write(f"测试模块: {filename}\n")
            f.write(f"结果: {status}\n")
            f.write("=" * 80 + "\n\n")
            f.write(output)
            f.write("\n")

        end_time = datetime.now()
        duration = end_time - start_time

        f.write("\n\n")
        f.write("=" * 80 + "\n")
        f.write(f"测试结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"总模块数: {len(test_files)}\n")
        f.write(f"通过（PASS）: {total_passed}\n")
        f.write(f"失败（FAIL）: {total_failed}\n")
        f.write(f"总耗时: {duration.total_seconds():.1f} 秒\n")
        f.write("=" * 80 + "\n")

    # 控制台输出
    print(f"\n日志已保存至: {log_path}")
    print(f"设备型号: {DEVICE_TYPE}")
    print(f"软件版本: {SOFTWARE_VERSION}")
    print(f"总计: {len(test_files)} 个模块 | PASS: {total_passed} | FAIL: {total_failed}")

    # 退出码：有任一失败则整体失败
    final_exit_code = 0 if total_failed == 0 else 1
    sys.exit(final_exit_code)


if __name__ == "__main__":
    main()