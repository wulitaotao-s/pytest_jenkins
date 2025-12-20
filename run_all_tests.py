# run_all_tests.py
import subprocess
import sys
import os
import re
from datetime import datetime

# === 固定配置 ===
BASE_REPORT_DIR = r"D:\pytest_jenkins\report"
os.makedirs(BASE_REPORT_DIR, exist_ok=True)

# 默认设备信息（如果无法提取）
DEVICE_TYPE = "UnknownDevice"
SOFTWARE_VERSION = "UnknownVersion"

# 设置 UTF-8 输出编码
if sys.version_info >= (3, 7):
    os.environ["PYTHONIOENCODING"] = "utf-8"

TEST_DIR = "Test_cases"


def extract_device_info_from_output(output_lines):
    """从输出中提取 Device Type 和 Software Version"""
    global DEVICE_TYPE, SOFTWARE_VERSION
    for line in output_lines:
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


def extract_module_name(line: str) -> str | None:
    match = re.search(r'[/\\]([^/\\]+\.py)::', line)
    return match.group(1) if match else None


def main():
    global DEVICE_TYPE, SOFTWARE_VERSION

    # 先运行一次 pytest --collect-only 获取设备信息（可选优化）
    # 但为简化，我们直接在正式运行中提取

    start_time = datetime.now()
    date_str = start_time.strftime('%Y-%m-%d')

    # 构建 pytest 命令
    cmd = [
        sys.executable, "-m", "pytest",
        "-v", "-s",
        "--tb=long",  # 确保显示完整 traceback
        TEST_DIR
    ]

    # 启动子进程
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,
        universal_newlines=True
    )

    all_output_lines = []

    try:
        for line in iter(process.stdout.readline, ""):
            all_output_lines.append(line)
    except Exception as e:
        all_output_lines.append(f"ERROR DURING CAPTURE: {e}\n")
    finally:
        process.wait()
        remaining = process.stdout.read()
        if remaining:
            all_output_lines.extend(remaining.splitlines(keepends=True))

    # 提取设备信息
    extract_device_info_from_output(all_output_lines)

    # 构建日志文件名
    safe_device = "".join(c if c.isalnum() or c in (" ", ".", "-", "_") else "_" for c in DEVICE_TYPE)
    safe_version = "".join(c if c.isalnum() or c in (" ", ".", "-", "_") else "_" for c in SOFTWARE_VERSION)
    log_filename = f"{date_str} {safe_device} {safe_version}.log"
    log_path = os.path.join(BASE_REPORT_DIR, log_filename)

    # 写入日志
    with open(log_path, "w", encoding="utf-8") as f:
        # 开头信息
        f.write(f"测试开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"设备型号: {DEVICE_TYPE}\n")
        f.write(f"软件版本: {SOFTWARE_VERSION}\n")
        f.write("=" * 80 + "\n\n")

        printed_modules = set()

        for line in all_output_lines:
            # 检测是否是新测试模块开始
            module = extract_module_name(line)
            if module and module not in printed_modules:
                f.write("\n\n")
                f.write("=" * 80 + "\n")
                f.write(f"开始执行测试模块: {module}\n")
                f.write("=" * 80 + "\n\n")
                printed_modules.add(module)

            f.write(line)

        # 结尾汇总
        end_time = datetime.now()
        duration = end_time - start_time
        f.write("\n\n")
        f.write("=" * 80 + "\n")
        f.write(f"测试结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"总耗时: {duration.total_seconds():.1f} 秒\n")
        f.write(f"退出码: {process.returncode} (0 表示全部通过)\n")
        f.write("=" * 80 + "\n")

    # 打印到控制台
    print(f"日志已保存至: {log_path}")
    print(f"设备型号: {DEVICE_TYPE}")
    print(f"软件版本: {SOFTWARE_VERSION}")

    # 退出码传递
    sys.exit(process.returncode)


if __name__ == "__main__":
    main()