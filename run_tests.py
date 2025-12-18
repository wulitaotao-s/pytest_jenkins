# run_tests.py
import subprocess
import os
from datetime import datetime

# 配置
REPORT_DIR = r"D:\pytest_jenkins\report"
os.makedirs(REPORT_DIR, exist_ok=True)

# 生成带时间戳的日志文件名
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
log_file = os.path.join(REPORT_DIR, f"{timestamp}.log")

# 构造 pytest 命令
cmd = ["pytest", "-v", "-s", r".\Test_cases\test_device_info.py"]

# 执行并重定向输出到日志文件
with open(log_file, "w", encoding="utf-8") as f:
    result = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, text=True)

print(f"测试完成，日志已保存至: {log_file}")

# 可选：设置环境变量供 send_email.py 使用
os.environ["LATEST_LOG"] = log_file

# 自动发送邮件（可选）
# subprocess.run(["python", "send_email.py"])
