import os
import sys
import subprocess
import smtplib
import re
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path

# 从 Jenkins 环境变量读取配置
sender_email = os.getenv("QQ_EMAIL")
password = os.getenv("QQ_AUTH_CODE")
receiver_email = os.getenv("RECIPIENT")
report_root = os.getenv("REPORT_ROOT", r"D:\pytest_jenkins\Reports")

test_cases_dir = "Test_cases"
get_info_script = "test_get_info.py"

if not all([sender_email, password, receiver_email]):
    print("Error: Missing required environment variables")
    sys.exit(1)

def run_script(script_path):
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        return result
    except Exception as e:
        return type('Result', (), {'stdout': '', 'stderr': str(e), 'returncode': 1})()

def extract_device_info(output):
    device = version = "Unknown"
    match = re.search(r"Device Type:\s*(\S+)", output)
    if match:
        device = match.group(1).strip()
    match = re.search(r"Software Version:\s*(\S+)", output)
    if match:
        version = match.group(1).strip()
    return device, version

def parse_pytest_summary(stdout):
    match = re.search(r"(\d+)\s+passed,\s+(\d+)\s+failed", stdout)
    if match:
        return int(match.group(1)), int(match.group(2))
    passed = len(re.findall(r"\s+PASSED\s+", stdout))
    failed = len(re.findall(r"\s+FAILED\s+", stdout))
    return passed, failed

def send_email(subject, body):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.qq.com", 587, timeout=15)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print("Failed to send email: " + str(e))

def main():
    os.makedirs(report_root, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # 获取设备信息
    info_result = run_script(get_info_script)
    raw_output = (info_result.stdout or "") + "\n" + (info_result.stderr or "")
    cleaned_output = re.sub(r'\x1B$$@-_$$$$0-?]*[ -/]*[@-~]', '', raw_output)

    device_type, software_version = extract_device_info(cleaned_output)
    print("Device Type:", device_type)
    print("Software Version:", software_version)

    # 运行测试
    test_dir = Path(test_cases_dir)
    if not test_dir.exists():
        print("Test_cases directory not found")
        passed = failed = 0
        full_test_output = ""
    else:
        test_result = subprocess.run(
            [sys.executable, "-m", "pytest", str(test_dir), "-v", "--tb=short"],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        full_test_output = (test_result.stdout or "") + "\n" + (test_result.stderr or "")
        passed, failed = parse_pytest_summary(full_test_output)
        print("Test Result:", passed, "passed,", failed, "failed")

    # 保存日志到本地（仅用于归档，不发送）
    log_filename = f"{timestamp}_{device_type}_{software_version}.log"
    log_path = os.path.join(report_root, log_filename)
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("=== DEVICE INFO ===\n")
        f.write(cleaned_output)
        f.write("\n\n=== TEST CASES OUTPUT ===\n")
        f.write(full_test_output)
        f.write("\n\n=== SUMMARY ===\n")
        f.write("Device Type: " + device_type + "\n")
        f.write("Software Version: " + software_version + "\n")
        f.write("Summary: " + str(passed) + " passed, " + str(failed) + " failed\n")

    print("Log saved to:", log_path)

    # 发送纯文本邮件（无附件，无日志引用）
    subject = "[Jenkins CI] " + device_type + " " + software_version + " | PASS: " + str(passed) + " / FAIL: " + str(failed)
    body = "Automated Test Report\n\n" \
           "Device Type: " + device_type + "\n" \
           "Software Version: " + software_version + "\n" \
           "Test Result: " + str(passed) + " passed, " + str(failed) + " failed"

    send_email(subject, body)

if __name__ == "__main__":
    main()