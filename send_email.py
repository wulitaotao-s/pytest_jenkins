import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_test_summary():
    qq_email = os.environ['QQ_EMAIL']
    qq_auth_code = os.environ['QQ_AUTH_CODE']
    recipient = os.environ['RECIPIENT']
    json_file = os.environ['JSON_REPORT']

    if not os.path.exists(json_file):
        print(f"ERROR: JSON 报告文件不存在: {json_file}")
        exit(1)

    # 读取 JSON 报告
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # 统计结果
    total = len(data['tests'])
    passed = sum(1 for t in data['tests'] if t['outcome'] == 'passed')
    failed = sum(1 for t in data['tests'] if t['outcome'] == 'failed')
    skipped = sum(1 for t in data['tests'] if t['outcome'] == 'skipped')
    error = sum(1 for t in data['tests'] if t['outcome'] == 'error')

    # 构建邮件正文
    summary = f"""自动化测试结果汇总：

- 总用例数：{total}
- 通过（PASS）：{passed}
- 失败（FAIL）：{failed}
- 跳过（SKIPPED）：{skipped}
- 错误（ERROR）：{error}

构建状态：{'✅ 全部通过' if failed == 0 and error == 0 else '❌ 存在失败或错误'}

此邮件由 Jenkins 自动发送，请勿回复。
"""

    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = qq_email
    msg['To'] = recipient
    msg['Subject'] = f'[Jenkins] 测试结果汇总（PASS: {passed}, FAIL: {failed}）'

    msg.attach(MIMEText(summary, 'plain', 'utf-8'))

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
    send_test_summary()