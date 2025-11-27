import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_test_report():
    # 从环境变量读取配置
    qq_email = os.environ['QQ_EMAIL']
    qq_auth_code = os.environ['QQ_AUTH_CODE']
    recipient = os.environ['RECIPIENT']
    report_file = os.environ['REPORT_NAME']

    # 检查报告文件是否存在
    if not os.path.exists(report_file):
        print(f"ERROR: 报告文件不存在: {report_file}")
        exit(1)

    # 读取 HTML 报告内容
    with open(report_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 构建邮件
    msg = MIMEMultipart('alternative')
    msg['Subject'] = '[Jenkins] Pytest 自动化测试报告'
    msg['From'] = qq_email
    msg['To'] = recipient
    msg.attach(MIMEText(html_content, 'html', 'utf-8'))

    try:
        # 连接 QQ 邮箱 SMTP 服务器
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(qq_email, qq_auth_code)
        server.send_message(msg)
        server.quit()
        print("邮件发送成功！收件人:", recipient)
    except Exception as e:
        print("邮件发送失败:", str(e))
        exit(1)

if __name__ == '__main__':
    send_test_report()