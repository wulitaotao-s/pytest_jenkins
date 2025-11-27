import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def send_test_report():
    qq_email = os.environ['QQ_EMAIL']
    qq_auth_code = os.environ['QQ_AUTH_CODE']
    recipient = os.environ['RECIPIENT']
    report_file = os.environ['REPORT_NAME']

    if not os.path.exists(report_file):
        print(f"ERROR: 报告文件不存在: {report_file}")
        exit(1)

    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = qq_email
    msg['To'] = recipient
    msg['Subject'] = '[Jenkins] Pytest 测试报告（HTML附件）'

    # 邮件正文（纯文本）
    body = "您好！\n\n本次自动化测试已完成，详细报告请查收附件。\n\n- 共执行测试用例：10 个\n- 状态：全部通过 ✅\n\n此邮件由 Jenkins 自动发送，请勿回复。"
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    # 添加 HTML 报告作为附件
    with open(report_file, "rb") as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
    encoders.encode_base64(part)
    part.add_header(
        'Content-Disposition',
        f'attachment; filename= "{os.path.basename(report_file)}"'
    )
    msg.attach(part)

    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(qq_email, qq_auth_code)
        server.send_message(msg)
        server.quit()
        print("✅ 邮件发送成功！收件人:", recipient)
    except Exception as e:
        print("❌ 邮件发送失败:", str(e))
        exit(1)

if __name__ == '__main__':
    send_test_report()