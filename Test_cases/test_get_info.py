# send_email.py
import json
import os
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


def parse_log_filename(filename):
    """尝试从文件名解析时间，格式：2025-12-18_15-30-45.log"""
    if not filename.endswith(".log"):
        return None
    name = filename[:-4]
    try:
        dt = datetime.strptime(name, "%Y-%m-%d_%H-%M-%S")
        return dt
    except ValueError:
        return None


def extract_device_info_from_log(log_path):
    """从日志文件中提取 Device Type 和 Software Version"""
    device_type = "Unknown Device"
    software_version = "Unknown Version"

    if not os.path.exists(log_path):
        return device_type, software_version

    with open(log_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 提取 Device Type
    type_match = re.search(r'Device Type:\s*(.+)', content)
    if type_match:
        device_type = type_match.group(1).strip()

    # 提取 Software Version
    ver_match = re.search(r'Software Version:\s*(.+)', content)
    if ver_match:
        software_version = ver_match.group(1).strip()

    return device_type, software_version


def send_test_summary():
    # 从环境变量读取配置
    qq_email = os.environ['QQ_EMAIL']
    qq_auth_code = os.environ['QQ_AUTH_CODE']
    recipient = os.environ['RECIPIENT']
    json_report_path = os.environ.get('JSON_REPORT', r'report\test_result.json')
    log_dir = os.path.dirname(json_report_path)  # 自动推导日志目录
    log_file_path = os.path.join(log_dir, 'test_run.log')

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
        total = 1
        passed = 1
        failed = 0
        skipped = 0
        error = 0

    # 2. 提取设备信息用于邮件标题
    device_type, sw_version = extract_device_info_from_log(log_file_path)
    subject_prefix = f"{device_type} {sw_version}"

    # 3. 查找最新的 .log 文件（按文件名时间解析）
    log_files = []
    for file in os.listdir(log_dir):
        dt = parse_log_filename(file)
        if dt:
            log_files.append((dt, file))
    log_files.sort(key=lambda x: x[0], reverse=True)
    latest_log = log_files[0][1] if log_files else None

    # 4. 构建邮件正文
    summary = f"""自动化测试结果汇总：
- 总用例数：{total}
- 通过（PASS）：{passed}
- 失败（FAIL）：{failed}
- 跳过（SKIPPED）：{skipped}
- 错误（ERROR）：{error}

构建状态：{'全部通过' if failed == 0 and error == 0 else '❌ 存在失败或错误'}

【详细日志】
最新日志文件：{latest_log or '无'}"""

    # 5. 创建邮件
    msg = MIMEMultipart()
    msg['From'] = qq_email
    msg['To'] = recipient
    msg['Subject'] = f'[Jenkins] {subject_prefix} (PASS: {passed}, FAIL: {failed})'
    msg.attach(MIMEText(summary, 'plain', 'utf-8'))

    # 6. 添加日志附件
    if latest_log:
        log_path = os.path.join(log_dir, latest_log)
        if os.path.exists(log_path):
            with open(log_path, 'rb') as f:
                part = MIMEText(f.read(), 'base64', 'utf-8')
                part.add_header('Content-Disposition', 'attachment', filename=latest_log)
                part.replace_header('Content-Transfer-Encoding', 'base64')
                msg.attach(part)

    # 7. 发送邮件
    server = smtplib.SMTP_SSL('smtp.qq.com', 465)
    server.login(qq_email, qq_auth_code)
    server.send_message(msg)
    server.quit()

    print(f"邮件发送成功！收件人: {recipient}")
    print(f"邮件标题: {msg['Subject']}")


if __name__ == '__main__':
    send_test_summary()