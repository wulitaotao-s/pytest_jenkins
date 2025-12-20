# send_email.py
import json
import os
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


def parse_log_filename(filename):
    """解析日志文件名中的日期，格式：2025-12-20_*.log 或 2025-12-20 *.log"""
    if not filename.endswith(".log"):
        return None
    # 尝试匹配 2025-12-20 开头
    match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
    if match:
        try:
            dt = datetime.strptime(match.group(1), "%Y-%m-%d")
            return dt
        except:
            return None
    return None


def extract_device_info_from_filename(filename):
    """从文件名提取设备型号和版本号"""
    if not filename.endswith(".log"):
        return "Unknown", "Unknown"
    name = filename[:-4]  # 去掉 .log
    parts = name.split(' ', 2)  # 最多分成三部分：[日期, 型号, 版本]
    if len(parts) >= 3:
        return parts[1], parts[2]
    return "Unknown", "Unknown"


def send_test_summary():
    qq_email = os.environ['QQ_EMAIL']
    qq_auth_code = os.environ['QQ_AUTH_CODE']
    recipient = os.environ['RECIPIENT']
    report_dir = r'D:\pytest_jenkins\report'

    # 查找最新的日志文件（按日期）
    log_files = []
    for file in os.listdir(report_dir):
        dt = parse_log_filename(file)
        if dt:
            log_files.append((dt, file))
    log_files.sort(key=lambda x: x[0], reverse=True)
    latest_log = log_files[0][1] if log_files else None

    # 从日志文件名提取设备信息
    device_type, sw_version = extract_device_info_from_filename(latest_log or "")

    # 构建邮件标题
    subject_prefix = f"{device_type} {sw_version}"

    # 测试结果统计（可选：你也可以从 pytest 输出解析，但这里简化）
    total = passed = failed = skipped = error = 0
    if latest_log:
        log_path = os.path.join(report_dir, latest_log)
        with open(log_path, 'r', encoding='utf-8') as f:
            content = f.read()
            passed = content.count("PASSED")
            failed = content.count("FAILED")
            error = content.count("ERROR")
            skipped = content.count("SKIPPED")
            total = passed + failed + skipped + error

    # 邮件正文
    summary = f"""自动化测试结果汇总：
总用例数：{total}
通过（PASS）：{passed}
失败（FAIL）：{failed}
跳过（SKIPPED）：{skipped}
错误（ERROR）：{error}

构建状态：{'全部通过' if failed == 0 and error == 0 else '存在失败或错误'}

详细日志文件：{latest_log or '无'}"""

    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = qq_email
    msg['To'] = recipient
    msg['Subject'] = f'[Jenkins] {subject_prefix} (PASS: {passed}, FAIL: {failed})'
    msg.attach(MIMEText(summary, 'plain', 'utf-8'))

    # 添加附件
    if latest_log:
        log_path = os.path.join(report_dir, latest_log)
        if os.path.exists(log_path):
            with open(log_path, 'rb') as f:
                part = MIMEText(f.read(), 'base64', 'utf-8')
                part.add_header('Content-Disposition', 'attachment', filename=latest_log)
                part.replace_header('Content-Transfer-Encoding', 'base64')
                msg.attach(part)

    # 发送
    server = smtplib.SMTP_SSL('smtp.qq.com', 465)
    server.login(qq_email, qq_auth_code)
    server.send_message(msg)
    server.quit()

    print("邮件发送成功！收件人:", recipient)


if __name__ == '__main__':
    send_test_summary()