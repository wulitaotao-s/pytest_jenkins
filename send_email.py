# send_email.py
import os
import smtplib
import re
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def parse_device_info_from_env():
    # 从环境变量读取（由 Jenkins 设置）
    device = os.getenv("DEVICE_TYPE", "Unknown")
    version = os.getenv("SOFTWARE_VERSION", "Unknown")
    return device, version


def parse_test_output(test_log):
    passed = failed = 0
    failed_cases = []

    # 统计 PASSED/FAILED
    passed = len(re.findall(r"\s+PASSED\s+", test_log))
    failed = len(re.findall(r"\s+FAILED\s+", test_log))

    # 提取失败用例名称（格式：test_xxx.py::test_yyy FAILED）
    lines = test_log.splitlines()
    for line in lines:
        if "FAILED" in line and "::" in line:
            case = line.split()[0]  # 如 Test_cases/test_login.py::test_bad_password
            failed_cases.append(case)

    return passed, failed, failed_cases

def main():
    sender_email = os.getenv("QQ_EMAIL")
    password = os.getenv("QQ_AUTH_CODE")
    receiver_email = os.getenv("RECIPIENT")

    if not all([sender_email, password, receiver_email]):
        print("Missing email environment variables", file=sys.stderr)
        sys.exit(1)

    device_type, software_version = parse_device_info_from_env()

    # 读取测试日志（从 stdin 或临时文件，这里假设通过环境传入摘要）
    # 实际中，Jenkins 可将 run_all_tests 的输出保存为文件供此脚本读取
    test_output_file = os.getenv("TEST_OUTPUT_FILE", "")
    test_log = ""
    if test_output_file and os.path.exists(test_output_file):
        with open(test_output_file, "r", encoding="utf-8") as f:
            test_log = f.read()
    else:
        # 若无文件，则尝试从环境变量（备用）
        test_log = os.getenv("TEST_SUMMARY", "")

    passed, failed, failed_cases = parse_test_output(test_log)

    # 构建邮件正文
    subject = f"[Jenkins CI] {device_type} {software_version} : PASS: {passed} | FAIL: {failed}"

    body_lines = []
    body_lines.append("Automated Test Report")
    body_lines.append("")
    body_lines.append(f"Device Type: {device_type}")
    body_lines.append(f"Software Version: {software_version}")
    body_lines.append(f"Test Result: {passed} passed, {failed} failed")
    if failed_cases:
        body_lines.append("")
        body_lines.append("Failed Test Cases:")
        for case in failed_cases:
            body_lines.append(f"- {case}")

    body = "\n".join(body_lines)

    # 发送邮件
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
        print("Failed to send email: " + str(e), file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()