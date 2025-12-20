# send_email.py
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import re


def get_test_summary(log_path):
    """从日志文件中提取测试结果"""
    passed = failed = 0
    device = version = "Unknown"
    if not log_path.exists():
        return device, version, passed, failed

    # 从文件名提取设备和版本（假设格式：2025-12-20_15-05-43 FT-35 V1.0.13.log）
    stem = log_path.stem
    parts = stem.split(' ', 2)
    device = parts[1] if len(parts) > 1 else "Unknown"
    version = parts[2] if len(parts) > 2 else "Unknown"

    # 从内容提取 Summary 行
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                if "Summary:" in line and "passed" in line and "failed" in line:
                    match = re.search(r"(\d+)\s+passed,\s+(\d+)\s+failed", line)
                    if match:
                        passed = int(match.group(1))
                        failed = int(match.group(2))
                        break
    except Exception as e:
        print(f"Error reading log: {e}")

    return device, version, passed, failed


def main():
    # 从 Jenkins environment 读取
    sender_email = os.getenv("QQ_EMAIL")
    password = os.getenv("QQ_AUTH_CODE")
    receiver_email = os.getenv("RECIPIENT")
    log_file = os.getenv("LOG_FILE")

    if not all([sender_email, password, receiver_email, log_file]):
        print("❌ Missing required environment variables: QQ_EMAIL, QQ_AUTH_CODE, RECIPIENT, LOG_FILE")
        exit(1)

    log_path = Path(log_file)
    device, version, passed, failed = get_test_summary(log_path)

    # 构建邮件
    subject = f"[Jenkins CI] {device} {version} | PASS: {passed} / FAIL: {failed}"
    body = f"""\
Automated Test Report from Jenkins

Device Type: {device}
Software Version: {version}
Test Result: {passed} passed, {failed} failed
Log File: {log_path.name}

Report generated at: {log_path.parent}
"""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        print(f"Connecting to smtp.qq.com:587...")
        server = smtplib.SMTP("smtp.qq.com", 587, timeout=15)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("✅ Email sent successfully.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        exit(1)  # 让 post 阶段失败（可选）


if __name__ == "__main__":
    main()