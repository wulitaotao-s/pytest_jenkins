import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from bs4 import BeautifulSoup

def main():
    if len(sys.argv) != 6:
        print("Usage: python send_email.py <start_time> <end_time> <passed_list_str> <failed_list_str> <html_report_file>")
        sys.exit(1)

    start_time = sys.argv[1] or "未知"
    end_time = sys.argv[2] or "未知"
    html_report_file = sys.argv[5]

    passed_tests = []
    failed_tests = []

    try:
        with open(html_report_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # 关键修正：使用 class_='results-table'（不是 id）
        table = soup.find('table', class_='results-table')
        if not table:
            print("Warning: No table with class 'results-table' found.", file=sys.stderr)
            return

        for row in table.find_all('tr'):
            classes = row.get('class', [])
            name_cell = row.find('td', class_='col-name')
            if name_cell:
                full_name = name_cell.get_text(strip=True)
                if 'passed' in classes:
                    passed_tests.append(full_name)
                elif 'failed' in classes or 'error' in classes:
                    failed_tests.append(full_name)
    except Exception as e:
        print(f"Failed to parse HTML report: {e}", file=sys.stderr)

    # 构建邮件正文
    body_lines = [
        "Jenkins 自动化测试报告",
        "",
        f"测试开始时间：{start_time}",
        f"测试结束时间：{end_time}",
        "",
        f"通过用例（{len(passed_tests)} 个）："
    ]

    if passed_tests:
        for test in passed_tests:
            body_lines.append(f"  • {test}")
    else:
        body_lines.append("  （无）")

    body_lines.append("")
    body_lines.append(f"失败用例（{len(failed_tests)} 个）：")

    if failed_tests:
        for test in failed_tests:
            body_lines.append(f"  • {test}")
    else:
        body_lines.append("  （无）")

    body = "\n".join(body_lines)

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