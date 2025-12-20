import os
import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def parse_test_output(test_log):
    passed = len([line for line in test_log.splitlines() if "PASSED" in line])
    failed = len([line for line in test_log.splitlines() if "FAILED" in line])
    failed_cases = []
    for line in test_log.splitlines():
        if "FAILED" in line and "::" in line:
            case = line.split()[0]
            failed_cases.append(case)
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
        f"Total Failed: {failed}"
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