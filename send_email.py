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

    html_report_file = sys.argv[5]

    start_time = ""
    end_time = ""
    passed_tests = []
    failed_tests = []

    try:
        with open(html_report_file, 'r', encoding='utf-8') as f:
            soup = BeautifulSoup(f, 'html.parser')

        # 尝试提取时间（pytest-html 通常在 summary 表格中）
        summary_table = soup.find('table', class_='summary')
        if summary_table:
            rows = summary_table.find_all('tr')
            for row in rows:
                cells = row.find_all('td')
                if len(cells) >= 2:
                    key = cells[0].get_text(strip=True)
                    value = cells[1].get_text(strip=True)
                    if 'Start Time' in key or '开始时间' in key:
                        start_time = value
                    elif 'Duration' in key or '运行时间' in key:
                        end_time = value  # 注意：这里实际是持续时间，非结束时间

        # 如果无法获取精确结束时间，可留空或用当前时间（此处简化处理）

        # 提取测试用例
        for row in soup.find_all('tr', class_=lambda x: x and ('passed' in x or 'failed' in x or 'error' in x)):
            name_cell = row.find('td', class_='col-name')
            if name_cell:
                test_name = name_cell.get_text(strip=True).split('::')[-1]  # 只取函数名
                full_name = name_cell.get_text(strip=True)
                classes = ' '.join(row.get('class', []))
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
        f"测试开始时间：{start_time or '未知'}",
        f"测试结束时间：{end_time or '未知'}",
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

    body_lines.append(f"通过用例（{len(passed_tests)} 个）：")
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