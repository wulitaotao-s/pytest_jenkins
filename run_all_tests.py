import os
import sys
import subprocess
import smtplib
import re
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path

# 从 Jenkins 环境变量获取配置
sender_email = os.getenv("QQ_EMAIL")
password = os.getenv("QQ_AUTH_CODE")
receiver_email = os.getenv("RECIPIENT")
report_root = os.getenv("REPORT_ROOT", r"D:\pytest_jenkins\Reports")  # 可选默认路径

test_cases_dir = "Test_cases"
get_info_script = "test_get_info.py"

if not all([sender_email, password, receiver_email]):
    print("Error: Missing required environment variables: QQ_EMAIL, QQ_AUTH_CODE, or RECIPIENT")
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
        device = match.group(1)
    match = re.search(r"Software Version:\s*(\S+)", output)
    if match:
        version = match.group(1)
    return device, version

def parse_pytest_summary(stdout):
    passed = len(re.findall(r"\s+PASSED\s+", stdout))
    failed = len(re.findall(r"\s+FAILED\s+", stdout))
    return passed, failed

def send_email(subject, body, attachment_path=None):
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    if attachment_path and Path(attachment_path).exists():
        try:
            with open(attachment_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", f"attachment; filename={Path(attachment_path).name}")
            msg.attach(part)
        except Exception as e:
            print("Failed to attach log: " + str(e))

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

    print("Running test_get_info.py...")
    info_result = run_script(get_info_script)
    info_log = info_result.stdout
    if info_result.stderr:
        info_log += "\n[STDERR]\n" + info_result.stderr

    device_type, software_version = extract_device_info(info_log)
    print("Device Type: " + device_type)
    print("Software Version: " + software_version)

    test_dir = Path(test_cases_dir)
    if not test_dir.exists():
        print("Test_cases directory not found")
        passed = failed = 0
        full_test_output = ""
    else:
        print("Running test cases in " + str(test_dir) + "...")
        test_result = subprocess.run(
            [sys.executable, "-m", "pytest", str(test_dir), "-v", "--tb=short"],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        full_test_output = test_result.stdout
        if test_result.stderr:
            full_test_output += "\n[STDERR]\n" + test_result.stderr
        passed, failed = parse_pytest_summary(test_result.stdout)

    log_filename = f"{timestamp} {device_type} {software_version}.log"
    log_path = os.path.join(report_root, log_filename)

    with open(log_path, "w", encoding="utf-8") as f:
        f.write("=== Device Info ===\n")
        f.write(info_log)
        f.write("\n\n=== Test Cases Output ===\n")
        f.write(full_test_output)
        f.write("\n\n=== Summary ===\n")
        f.write(f"Device Type: {device_type}\n")
        f.write(f"Software Version: {software_version}\n")
        f.write(f"Summary: {passed} passed, {failed} failed\n")

    print("Log saved to: " + log_path)

    subject = "[Jenkins CI] " + device_type + " " + software_version + " | PASS: " + str(passed) + " / FAIL: " + str(failed)
    body = "Automated Test Report\n\n" \
           "Device Type: " + device_type + "\n" \
           "Software Version: " + software_version + "\n" \
           "Test Result: " + str(passed) + " passed, " + str(failed) + " failed\n" \
           "Log File: " + log_filename

    send_email(subject, body, log_path)

if __name__ == "__main__":
    main()