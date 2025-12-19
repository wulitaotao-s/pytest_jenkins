# run_all_tests.py
import subprocess
import sys
import os
from datetime import datetime

# 从环境变量读取，兼容 Jenkins
JSON_REPORT = os.getenv("JSON_REPORT", "report/test_result.json")
LOG_FILE = os.getenv("LOG_FILE", "test_run.log")
TEST_DIR = "Test_cases"  # 保持不变，因为 checkout 后就在根目录

# 确保报告目录存在
os.makedirs(os.path.dirname(JSON_REPORT), exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def main():
    start_time = datetime.now()
    print(f"测试开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # 清空日志
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"测试开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("="*60 + "\n\n")

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
            print(line, end="")
            log_f.write(line)
            log_f.flush()

        process.wait()

    end_time = datetime.now()
    duration = end_time - start_time
    summary = (
        f"\n\n{'='*60}\n"
        f"测试结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}\n"
        f"总耗时: {duration.total_seconds():.1f} 秒\n"
        f"{'='*60}\n"
    )
    print(summary)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(summary)

if __name__ == "__main__":
    main()