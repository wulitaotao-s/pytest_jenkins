# run_all_tests.py
import subprocess
import sys
import os
import re
from datetime import datetime

# === 配置 ===
# 优先读取环境变量，否则使用默认路径
REPORT_DIR = os.environ.get("REPORT_DIR", r"D:\pytest_jenkins\report")
JSON_REPORT = os.environ.get("JSON_REPORT", os.path.join(REPORT_DIR, "test_result.json"))
LOG_FILE = os.environ.get("LOG_FILE", os.path.join(REPORT_DIR, "test_run.log"))

# 确保目录存在
os.makedirs(REPORT_DIR, exist_ok=True)

# 设置 UTF-8 输出编码（防止中文乱码）
if sys.version_info >= (3, 7):
    os.environ["PYTHONIOENCODING"] = "utf-8"

TEST_DIR = "Test_cases"  # 测试用例目录


def extract_module_name(line: str) -> str | None:
    """从 pytest 输出中提取模块名，如 test_acs_connection.py"""
    match = re.search(r'[/\\]([^/\\]+\.py)::', line)
    return match.group(1) if match else None


def main():
    start_time = datetime.now()
    timestamp_str = start_time.strftime('%Y-%m-%d %H:%M:%S')

    # 初始化日志文件
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"测试开始时间: {timestamp_str}\n")
        f.write("=" * 60 + "\n\n")

    print(f"测试开始时间: {timestamp_str}")
    print("=" * 60)

    # 构建 pytest 命令
    cmd = [
        sys.executable, "-m", "pytest",
        "-v", "-s",
        "--json-report",
        f"--json-report-file={JSON_REPORT}",
        TEST_DIR
    ]

    printed_modules = set()

    # 启动子进程并实时捕获输出
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        encoding="utf-8",
        errors="replace",
        bufsize=1,  # 行缓冲
        universal_newlines=True
    )

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as log_f:
            for line in iter(process.stdout.readline, ""):
                module = extract_module_name(line)

                if module and module not in printed_modules:
                    separator = "\n" + "=" * 60 + "\n"
                    title = f">>> 开始执行测试模块: {module}\n"

                    # 控制台输出
                    print(separator, end="")
                    print(title, end="")
                    print(separator, end="")

                    # 写入日志
                    log_f.write(separator)
                    log_f.write(title)
                    log_f.write(separator)
                    log_f.flush()
                    printed_modules.add(module)

                # 写入原始行（含错误、堆栈等）
                log_f.write(line)
                log_f.flush()

    except Exception as e:
        print(f"⚠️ 读取 pytest 输出时发生异常: {e}")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"\n⚠️ 异常: {e}\n")

    finally:
        process.wait()  # 等待 pytest 结束
        # 读取可能残留的输出（确保不丢数据）
        remaining = process.stdout.read()
        if remaining:
            with open(LOG_FILE, "a", encoding="utf-8") as f:
                f.write(remaining)
                f.flush()

    # 写入总结信息
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

    # 关键：将 pytest 的退出码传递给操作系统
    sys.exit(process.returncode)


if __name__ == "__main__":
    main()