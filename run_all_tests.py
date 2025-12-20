# run_all_tests.py
import subprocess
import sys
import os
import re
from datetime import datetime
import json

# === 配置 ===
BASE_REPORT_DIR = r"D:\pytest_jenkins\report"
os.makedirs(BASE_REPORT_DIR, exist_ok=True)

# 设备信息（可从第一个文件输出中提取）
DEVICE_TYPE = "UnknownDevice"
SOFTWARE_VERSION = "UnknownVersion"

if sys.version_info >= (3, 7):
    os.environ["PYTHONIOENCODING"] = "utf-8"

TEST_DIR = "Test_cases"


def extract_device_info_from_output(output: str):
    global DEVICE_TYPE, SOFTWARE_VERSION
    lines = output.splitlines()
    for line in lines:
        if "Device Type:" in line:
            try:
                DEVICE_TYPE = line.split("Device Type:")[-1].strip()
            except:
                pass
        if "Software Version:" in line:
            try:
                SOFTWARE_VERSION = line.split("Software Version:")[-1].strip()
            except:
                pass


def get_test_files():
    """获取所有 test_*.py 文件"""
    files = []
    if not os.path.exists(TEST_DIR):
        print(f"错误：测试目录 {TEST_DIR} 不存在")
        return files
    for f in os.listdir(TEST_DIR):
        if f.startswith("test_") and f.endswith(".py"):
            files.append(f)
    return sorted(files)


def main():
    global DEVICE_TYPE, SOFTWARE_VERSION

    start_time = datetime.now()
    date_str = start_time.strftime('%Y-%m-%d')

    test_files = get_test_files()
    results = []

    # 先运行第一个文件以获取设备信息（可选）
    if test_files:
        first_file = os.path.join(TEST_DIR, test_files[0])
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-v", "-s", first_file],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace"
        )
        extract_device_info_from_output(result.stdout + result.stderr)
        # 重新加入结果列表
        results.append({
            'file': test_files[0],
            'returncode': result.returncode,
            'output': result.stdout + result.stderr
        })

        # 运行其余文件
        for filename in test_files[1:]:
            filepath = os.path.join(TEST_DIR, filename)
            result = subprocess.run(
                [sys.executable, "-m", "pytest", "-v", "-s", filepath],
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace"
            )
            results.append({
                'file': filename,
                'returncode': result.returncode,
                'output': result.stdout + result.stderr
            })
    else:
        print("未找到任何测试文件")
        sys.exit(1)

    # 构建日志文件名
    safe_device = "".join(c if c.isalnum() or c in (" ", ".", "-", "_") else "_" for c in DEVICE_TYPE)
    safe_version = "".join(c if c.isalnum() or c in (" ", ".", "-", "_") else "_" for c in SOFTWARE_VERSION)
    log_filename = f"{date_str} {safe_device} {safe_version}.log"
    log_path = os.path.join(BASE_REPORT_DIR, log_filename)

    passed = 0
    failed = 0

    with open(log_path, "w", encoding="utf-8") as f:
        f.write(f"测试开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"设备型号: {DEVICE_TYPE}\n")
        f.write(f"软件版本: {SOFTWARE_VERSION}\n")
        f.write("=" * 80 + "\n\n")

        for item in results:
            filename = item['file']
            returncode = item['returncode']
            output = item['output']

            status = "PASS" if returncode == 0 else "FAIL"
            if returncode == 0:
                passed += 1
            else:
                failed += 1

            f.write("\n\n")
            f.write("=" * 80 + "\n")
            f.write(f"测试模块: {filename}\n")
            f.write(f"结果: {status}\n")
            f.write("=" * 80 + "\n\n")

            f.write(output)
            f.write("\n")

        end_time = datetime.now()
        duration = end_time - start_time
        total = len(results)

        f.write("\n\n")
        f.write("=" * 80 + "\n")
        f.write(f"测试结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"总用例数: {total}\n")
        f.write(f"通过（PASS）: {passed}\n")
        f.write(f"失败（FAIL）: {failed}\n")
        f.write(f"总耗时: {duration.total_seconds():.1f} 秒\n")
        f.write("=" * 80 + "\n")

    # 打印到控制台
    print(f"日志已保存至: {log_path}")
    print(f"设备型号: {DEVICE_TYPE}")
    print(f"软件版本: {SOFTWARE_VERSION}")
    print(f"总计: {total} 个模块, PASS: {passed}, FAIL: {failed}")

    # 生成简化版 JSON 报告（兼容 send_email.py）
    json_report_path = os.path.join(BASE_REPORT_DIR, "test_result.json")
    json_data = {
        "summary": {
            "total": total,
            "passed": passed,
            "failed": failed,
            "skipped": 0,
            "error": 0
        },
        "tests": [
            {
                "nodeid": item['file'],
                "outcome": "passed" if item['returncode'] == 0 else "failed"
            }
            for item in results
        ]
    }
    with open(json_report_path, "w", encoding="utf-8") as jf:
        json.dump(json_data, jf, ensure_ascii=False, indent=2)

    # 退出码：只要有一个失败，整体返回非0
    final_exit_code = 0 if failed == 0 else 1
    sys.exit(final_exit_code)


if __name__ == "__main__":
    main()