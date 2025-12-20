# send_email.py
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path


def extract_device_info_from_filename(filename):
    name = filename.replace(".log", "")
    parts = name.split(' ', 2)
    device = parts[1] if len(parts) > 1 else "UnknownDevice"
    version = parts[2] if len(parts) > 2 else "UnknownVersion"
    return device.strip(), version.strip()


def parse_test_summary_from_log(log_content):
    lines = log_content.splitlines()
    for line in lines:
        if "Passed:" in line and "Failed:" in line:
            import re
            match = re.search(r"(\d+)\s+passed,\s+(\d+)\s+failed", line)
            if match:
                return int(match.group(1)), int(match.group(2))
    return 0, 0


def send_test_report_email(log_file_path):
    log_path = Path(log_file_path)
    if not log_path.exists():
        raise FileNotFoundError(f"Log file not found: {log_file_path}")

    device, version = extract_device_info_from_filename(log_path.name)

    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()

    passed, failed = parse_test_summary_from_log(content)

    # 邮件配置（请根据实际情况修改）
    smtp_server = "smtp.example.com"
    smtp_port = 587
    sender_email = "your_email@example.com"
    sender_password = os.getenv("EMAIL_PASSWORD")  # 建议用环境变量
    receiver_email = "team@example.com"

    subject = f"[Jenkins] {device} {version} | PASS: {passed} / FAIL: {failed}"
    body = f"""\
Automated test report for device: {device} (Version: {version})

Summary:
- Passed: {passed}
- Failed: {failed}
- Log file: {log_path.name}
"""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise