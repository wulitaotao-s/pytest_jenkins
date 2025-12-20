# run_all_tests.py
import subprocess
import sys
import os
import re
from datetime import datetime

if sys.version_info >= (3, 7):
    os.environ["PYTHONIOENCODING"] = "utf-8"

TEST_DIR = "Test_cases"
BASE_DIR = os.getcwd()
REPORT_DIR = os.path.join(BASE_DIR, "report")
os.makedirs(REPORT_DIR, exist_ok=True)

JSON_REPORT = os.path.join(REPORT_DIR, "test_result.json")
LOG_FILE = os.path.join(REPORT_DIR, "test_run.log")


def extract_module_name(line: str) -> str | None:
    # 正确匹配 Test_cases/test_xxx.py:: 或 Test_cases\test_xxx.py::
    match = re.search(r'[/\\]([^/\\]+\.py)::', line)
    return match.group(1) if match else None


def main():
    start_time = datetime.now()
    timestamp_str = start_time.strftime('%Y-%m-%d %H:%M:%S')

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"测试开始时间: {timestamp_str}\n")
        f.write("=" * 60 + "\n\n")

    print(f"测试开始时间: {timestamp_str}")
    print("=" * 60)

    cmd = [
        sys.executable, "-m", "pytest",
        "-v", "-s",
        "--json-report",
        f"--json-report-file={JSON_REPORT}",
        TEST_DIR
    ]

    printed_modules = set()

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
            module = extract_module_name(line)

            if module and module not in printed_modules:
                separator = "\n" + "=" * 60 + "\n"
                title = f">>> 开始执行测试模块: {module}\n"

                # 控制台输出
                print(separator, end="")
                print(title, end="")
                print(separator, end="")

                # 日志写入
                log_f.write(separator)
                log_f.write(title)
                log_f.write(separator)
                log_f.flush()
                printed_modules.add(module)

            # 只写日志，不重复 print 到控制台
            log_f.write(line)
            log_f.flush()

        process.wait()

    end_time = datetime.now()
    duration = end_time - start_time
    summary = (
        f"\n{'=' * 60}\n"
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