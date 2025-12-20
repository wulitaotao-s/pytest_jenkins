# send_email.py
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path


def extract_device_info_from_filename(filename: str):
    """从日志文件名 '2025-12-20_14-05-29 FT-35 V1.0.13.log' 提取设备信息"""
    name = filename.replace(".log", "")
    parts = name.split(' ', 2)  # 最多分3部分
    device = parts[1] if len(parts) > 1 else "UnknownDevice"
    version = parts[2] if len(parts) > 2 else "UnknownVersion"
    return device.strip(), version.strip()


def parse_test_summary_from_log(log_content: str):
    """从日志内容中解析通过/失败数量"""
    lines = log_content.splitlines()
    for line in lines:
        if "Summary:" in line or ("Passed:" in line and "Failed:" in line):
            # 例如: Summary: 2 passed, 1 failed
            import re
            match = re.search(r"(\d+)\s+passed,\s+(\d+)\s+failed", line)
            if match:
                passed = int(match.group(1))
                failed = int(match.group(2))
                return passed, failed
    return 0, 0


def send_test_report_email(log_file_path: str):
    log_path = Path(log_file_path)
    if not log_path.exists():
        raise FileNotFoundError(f"Log file not found: {log_file_path}")

    # 提取设备信息
    device, version = extract_device_info_from_filename(log_path.name)

    # 读取日志内容
    with open(log_path, "r", encoding="utf-8") as f:
        content = f.read()

    # 解析统计
    passed, failed = parse_test_summary_from_log(content)

    # 邮件配置（请替换为你的实际配置）
    smtp_server = "smtp.example.com"
    smtp_port = 587
    sender_email = "your_email@example.com"
    sender_password = "your_app_password"  # 建议用环境变量
    receiver_email = "team@example.com"

    # 构建邮件
    subject = f"[Jenkins] {device} {version} | PASS: {passed} / FAIL: {failed}"
    body = f"""\
Automated test report for device: {device} (Version: {version})

Summary:
- Passed: {passed}
- Failed: {failed}
- Log file: {log_path.name}

Full log attached.
"""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    msg.attach(MIMEText(body, "plain"))

    # 可选：附加日志文件
    # from email.mime.base import MIMEBase
    # from email import encoders
    # with open(log_path, "rb") as attachment:
    #     part = MIMEBase("application", "octet-stream")
    #     part.set_payload(attachment.read())
    # encoders.encode_base64(part)
    # part.add_header("Content-Disposition", f"attachment; filename= {log_path.name}")
    # msg.attach(part)

    # 发送邮件
    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Email sent successfully.")
    except Exception as e:
        print(f"Failed to send email: {e}")
        raise