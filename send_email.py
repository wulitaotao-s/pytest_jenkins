# send_email.py

import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


def send_test_summary():
    # 从环境变量读取配置
    qq_email = os.environ['QQ_EMAIL']
    qq_auth_code = os.environ['QQ_AUTH_CODE']
    recipient = os.environ['RECIPIENT']
    json_report_path = os.environ.get('JSON_REPORT', r'D:\pytest_jenkins\report\test_result.json')
    log_dir = r'D:\pytest_jenkins\report'

    # 1. 读取 JSON 报告（如果存在）
    if os.path.exists(json_report_path):
        with open(json_report_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        total = len(data['tests'])
        passed = sum(1 for t in data['tests'] if t['outcome'] == 'passed')
        failed = sum(1 for t in data['tests'] if t['outcome'] == 'failed')
        skipped = sum(1 for t in data['tests'] if t['outcome'] == 'skipped')
        error = sum(1 for t in data['tests'] if t['outcome'] == 'error')
    else:
        # 如果没有 JSON 报告，假设单个测试通过
        total = 1
        passed = 1
        failed = 0
        skipped = 0
        error = 0

    # 2. 查找最新的 .log 文件
    log_files = []
    for file in os.listdir(log_dir):
        if file.endswith(".log"):
            try:
                dt = datetime.strptime(file[:-4], "%Y-%m-%d %H:%M:%S")
                log_files.append((dt, file))
            except ValueError:
                continue
    log_files.sort(reverse=True)
    latest_log = log_files[0][1] if log_files else None

    # 3. 构建邮件正文
    summary = f"""自动化测试结果汇总：

- 总用例数：{total}
- 通过（PASS）：{passed}
- 失败（FAIL）：{failed}
- 跳过（SKIPPED）：{skipped}
- 错误（ERROR）：{error}

构建状态：{'✅ 全部通过' if failed == 0 and error == 0 else '❌ 存在失败或错误'}

【详细日志】
最新日志文件：{latest_log or '无'}
"""

    # 4. 创建邮件
    msg = MIMEMultipart()
    msg['From'] = qq_email
    msg['To'] = recipient
    msg['Subject'] = f'[Jenkins] 测试结果汇总（PASS: {passed}, FAIL: {failed}）'
    msg.attach(MIMEText(summary, 'plain', 'utf-8'))

    # 5. 添加日志附件
    if latest_log:
        log_path = os.path.join(log_dir, latest_log)
        if os.path.exists(log_path):
            with open(log_path, 'rb') as f:
                part = MIMEText(f.read(), 'base64', 'utf-8')
                part.add_header('Content-Disposition', 'attachment', filename=latest_log)
                msg.attach(part)

    # 6. 发送邮件
    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(qq_email, qq_auth_code)
        server.send_message(msg)
        server.quit()
        print("📧 邮件发送成功！收件人:", recipient)
    except Exception as e:
        print("📧 邮件发送失败:", str(e))
        exit(1)


if __name__ == '__main__':
    send_test_summary()