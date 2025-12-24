import sys
import os
import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def extract_summary_counts(html_content):
    """
    从 HTML 的 Summary 部分提取 Passed / Failed 数量
    匹配类似: "4 Failed, 3 Passed, 0 Skipped"
    """
    passed = failed = 0

    # 查找 Summary 行（通常在 <p class="filter"> 或文本中）
    summary_match = re.search(r'(\d+)\s+Failed,\s+(\d+)\s+Passed', html_content)
    if summary_match:
        failed = int(summary_match.group(1))
        passed = int(summary_match.group(2))
    else:
        # 备用：分别匹配
        failed_match = re.search(r'(\d+)\s+Failed', html_content)
        passed_match = re.search(r'(\d+)\s+Passed', html_content)
        if failed_match:
            failed = int(failed_match.group(1))
        if passed_match:
            passed = int(passed_match.group(1))

    return passed, failed

def main():
    if len(sys.argv) != 6:
        print("Usage: python send_email.py <start_time> <end_time> <...> <html_report_file>")
        sys.exit(1)

    start_time = sys.argv[1] or "未知"
    end_time = sys.argv[2] or "未知"
    html_report_file = sys.argv[5]

    passed = failed = 0

    try:
        with open(html_report_file, 'r', encoding='utf-8') as f:
            content = f.read()
        passed, failed = extract_summary_counts(content)
    except Exception as e:
        print(f"Failed to parse HTML report: {e}", file=sys.stderr)

    # 构建简洁邮件正文
    body = f"""Jenkins 自动化测试报告

测试开始时间：{start_time}
测试结束时间：{end_time}

通过用例：{passed} 个
失败用例：{failed} 个
"""

    sender_email = os.getenv("QQ_EMAIL")
    password = os.getenv("QQ_AUTH_CODE")
    receiver_email = os.getenv("RECIPIENT")

    if not all([sender_email, password, receiver_email]):
        print("Error: Missing required environment variables", file=sys.stderr)
        sys.exit(1)

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Jenkins测试报告"

    msg.attach(MIMEText(body, "plain", "utf-8"))

    # 添加附件
    if os.path.exists(html_report_file):
        with open(html_report_file, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        filename = os.path.basename(html_report_file)
        part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
        msg.attach(part)

    # 发送邮件
    try:
        server = smtplib.SMTP("smtp.qq.com", 587, timeout=15)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
    sys.exit(0)