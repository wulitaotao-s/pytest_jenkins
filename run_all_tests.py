# run_all_tests.py
import subprocess
import sys
import os
import re
from datetime import datetime
os.environ['PYTHONIOENCODING'] = 'utf-8'

# === 配置 ===
JSON_REPORT = os.getenv("JSON_REPORT", "report/test_result.json")
LOG_FILE = os.getenv("LOG_FILE", "test_run.log")
TEST_DIR = "Test_cases"

os.makedirs(os.path.dirname(JSON_REPORT), exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# 记录当前已打印的模块，避免重复
printed_modules = set()


def extract_module_name(line: str) -> str | None:
    """从 pytest -v 输出中提取 test_xxx.py"""
    match = re.search(r'^(\w+\.py)::', line)
    if match:
        return match.group(1)
    return None


def main():
    start_time = datetime.now()
    timestamp_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
    header = f"测试开始时间: {timestamp_str}"
    print(header)

    # 初始化日志文件
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(header + "\n")
        f.write("=" * 60 + "\n\n")

    cmd = [
        sys.executable, "-m", "pytest",
        "-v", "-s",
        "--json-report",
        f"--json-report-file={JSON_REPORT}",
        TEST_DIR
    ]

    with open(LOG_FILE, "a", encoding="utf-8") as log_f:
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        for line in iter(process.stdout.readline, ""):
            # 尝试提取模块名
            module = extract_module_name(line)
            if module and module not in printed_modules:
                separator = (
                        "\n" + "=" * 60 + "\n"
                                          f"开始执行测试模块: {module}\n"
                        + "=" * 60 + "\n"
                )
                print(separator, end="")
                log_f.write(separator)
                log_f.flush()
                printed_modules.add(module)

            # 输出原始行（包括 print 内容）
            print(line, end="")
            log_f.write(line)
            log_f.flush()

        process.wait()

    # 结束信息
    end_time = datetime.now()
    duration = end_time - start_time
    summary = (
        f"\n\n{'=' * 60}\n"
        f"测试结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"总耗时: {duration.total_seconds():.1f} 秒\n"
        f"退出码: {process.returncode} (0=成功)\n"
        f"{'=' * 60}\n"
    )
    print(summary)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(summary)


if __name__ == "__main__":
    main()