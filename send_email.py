import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def main():
    if len(sys.argv) != 6:
        print("Usage: python send_email.py <start_time> <end_time> <passed_list_str> <failed_list_str> <html_report_file>")
        sys.exit(1)

    start_time = sys.argv[1]
    end_time = sys.argv[2]
    passed_list_str = sys.argv[3]
    failed_list_str = sys.argv[4]
    html_report_file = sys.argv[5]

    # 拆分为列表，过滤空项
    passed_list = [t.strip() for t in passed_list_str.split(',') if t.strip()]
    failed_list = [t.strip() for t in failed_list_str.split(',') if t.strip()]

    # 从环境变量获取邮件配置
    sender_email = os.getenv("QQ_EMAIL")
    password = os.getenv("QQ_AUTH_CODE")
    receiver_email = os.getenv("RECIPIENT")

    if not all([sender_email, password, receiver_email]):
        print("Error: Missing required environment variables: QQ_EMAIL, QQ_AUTH_CODE, RECIPIENT", file=sys.stderr)
        sys.exit(1)

    # 构建邮件正文
    body_lines = []
    body_lines.append("Jenkins 自动化测试报告")
    body_lines.append("")
    body_lines.append(f"测试开始时间：{start_time}")
    body_lines.append(f"测试结束时间：{end_time}")
    body_lines.append("")
    body_lines.append(f"通过用例（{len(passed_list)} 个）：")
    if passed_list:
        for test in passed_list:
            body_lines.append(f"  • {test}")
    else:
        body_lines.append("  （无）")

    body_lines.append("")
    body_lines.append(f"失败用例（{len(failed_list)} 个）：")
    if failed_list:
        for test in failed_list:
            body_lines.append(f"  • {test}")
    else:
        body_lines.append("  （无）")

    body = "\n".join(body_lines)

    # 创建邮件对象
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = "Jenkins测试报告"

    # 添加纯文本正文（UTF-8）
    msg.attach(MIMEText(body, "plain", "utf-8"))

    # 添加 HTML 报告附件（如果存在）
    if html_report_file and os.path.exists(html_report_file):
        with open(html_report_file, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        filename = os.path.basename(html_report_file)
        part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
        msg.attach(part)
    else:
        print(f"Warning: HTML report not found at {html_report_file}", file=sys.stderr)

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