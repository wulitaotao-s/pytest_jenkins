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

    # 检查文件是否存在
    if not os.path.exists(report_file):
        print("ERROR: Report file not found:", report_file)
        return

    # 读取 HTML 报告
    with open(report_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 创建邮件
    msg = MIMEMultipart('alternative')
    msg['Subject'] = '[Jenkins] Pytest 测试报告'
    msg['From'] = qq_email
    msg['To'] = recipient
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))

    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(qq_email, qq_auth_code)
        server.send_message(msg)
        server.quit()
        print("邮件发送成功！收件人:", recipient)  # 使用纯文本
    except Exception as e:
        print("邮件发送失败:", str(e))
        raise  # 确保构建失败

if __name__ == '__main__':
    send_test_report()