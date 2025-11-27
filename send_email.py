# send_email.py
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_test_report():
    qq_email = os.environ['QQ_EMAIL']
    qq_auth_code = os.environ['QQ_AUTH_CODE']
    recipient = os.environ['RECIPIENT']
    report_file = os.environ['REPORT_NAME']

    # 读取 HTML 报告
    with open(report_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 构建邮件
    msg = MIMEMultipart('alternative')
    msg['Subject'] = '[Jenkins] Pytest 测试报告'
    msg['From'] = qq_email
    msg['To'] = recipient
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))

    # 发送
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