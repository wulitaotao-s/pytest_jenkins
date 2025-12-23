import os
import smtplib
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

def main():
    sender_email = os.getenv("QQ_EMAIL")
    password = os.getenv("QQ_AUTH_CODE")
    receiver_email = os.getenv("RECIPIENT")
    html_report_file = os.getenv("HTML_REPORT_FILE")  # 注意：现在用 HTML 报告路径

    # 检查必要环境变量
    if not all([sender_email, password, receiver_email, html_report_file]):
        print("Missing required environment variables", file=sys.stderr)
        sys.exit(1)

    # 创建邮件对象
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = ""  # 标题为空

    # 正文为空
    msg.attach(MIMEText("", "plain"))

    # 添加 HTML 报告作为附件（如果存在）
    if os.path.exists(html_report_file):
        with open(html_report_file, "rb") as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
        encoders.encode_base64(part)
        filename = os.path.basename(html_report_file)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename="{filename}"'
        )
        msg.attach(part)
    else:
        # 如果报告不存在，至少发个空邮件（或可选择不发）
        print(f"Warning: HTML report not found at {html_report_file}", file=sys.stderr)

    # 发送邮件
    try:
        server = smtplib.SMTP("smtp.qq.com", 587, timeout=15)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email with HTML report sent successfully")
    except Exception as e:
        print(f"Failed to send email: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()