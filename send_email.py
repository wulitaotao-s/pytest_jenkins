import os
import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def parse_test_output(test_log):
    passed = 0
    failed = 0
    failed_cases = []

    for line in test_log.splitlines():
        # 只匹配以测试文件路径开头、包含 :: 的行（pytest -v 格式）
        # 例如: test_login.py::test_valid_login PASSED
        if "::" in line and ("PASSED" in line or "FAILED" in line or "ERROR" in line):
            parts = line.strip().split()
            if not parts:
                continue
            status = parts[-1]  # 最后一个词通常是状态
            test_name = parts[0]  # 第一个词是 test_file::test_func

            if status == "PASSED":
                passed += 1
            elif status in ("FAILED", "ERROR"):
                failed += 1
                failed_cases.append(test_name)

    return passed, failed, failed_cases

def main():
    sender_email = os.getenv("QQ_EMAIL")
    password = os.getenv("QQ_AUTH_CODE")
    receiver_email = os.getenv("RECIPIENT")
    test_output_file = os.getenv("TEST_OUTPUT_FILE")

    if not all([sender_email, password, receiver_email]):
        print("Missing email environment variables", file=sys.stderr)
        sys.exit(1)

    test_log = ""
    if test_output_file and os.path.exists(test_output_file):
        with open(test_output_file, "r", encoding="utf-8", errors="replace") as f:
            test_log = f.read()
    else:
        test_log = "[ERROR] Test log file not found or unreadable."

    passed, failed, failed_cases = parse_test_output(test_log)

    subject = f"[Jenkins CI] Test Result: PASS {passed} | FAIL {failed}"
    body_lines = [
        "Automated Test Report",
        "",
        f"Total Passed: {passed}",
        f"Total Failed (or Error): {failed}"
    ]
    if failed_cases:
        body_lines.append("")
        body_lines.append("Failed Test Cases:")
        for case in failed_cases:
            body_lines.append(f"- {case}")
    body = "\n".join(body_lines)

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