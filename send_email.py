# send_email.py
import os
import smtplib
import re
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime


def parse_log_filename(filename):
    """解析日志文件名中的日期，格式：2025-12-20 *.log"""
    if not filename.endswith(".log"):
        return None
    match = re.match(r'(\d{4}-\d{2}-\d{2})', filename)
    if match:
        try:
            return datetime.strptime(match.group(1), "%Y-%m-%d")
        except:
            pass
    return None


def extract_device_info_from_filename(filename):
    """从日志文件名提取设备型号和版本号"""
    if not filename or not filename.endswith(".log"):
        return "UnknownDevice", "UnknownVersion"
    name = filename[:-4]  # 去掉 .log
    parts = name.split(' ', 2)  # [日期, 型号, 版本]
    device = parts[1] if len(parts) > 1 else "UnknownDevice"
    version = parts[2] if len(parts) > 2 else "UnknownVersion"
    return device.strip(), version.strip()


def read_summary_from_log(log_path):
    """从日志末尾提取汇总信息"""
    try:
        with open(log_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        total = passed = failed = 0
        for line in lines[-20:]:  # 只看最后20行
            if "总用例数:" in line:
                total = int(re.search(r'\d+', line).group())
            elif "通过（PASS）:" in line:
                passed = int(re.search(r'\d+', line).group())
            elif "失败（FAIL）:" in line:
                failed = int(re.search(r'\d+', line).group())

        return total, passed, failed
    except Exception as e:
        print(f"读取日志摘要失败: {e}")
        return 0, 0, 0


def send_test_summary():
    try:
        qq_email = os.environ['QQ_EMAIL']
        qq_auth_code = os.environ['QQ_AUTH_CODE']
        recipient = os.environ['RECIPIENT']
    except KeyError as e:
        print(f"环境变量缺失: {e}")
        return

    report_dir = r'D:\pytest_jenkins\report'

    # 查找最新的日志文件
    log_files = []
    for file in os.listdir(report_dir):
        dt = parse_log_filename(file)
        if dt:
            log_files.append((dt, file))

    if not log_files:
        print("未找到任何日志文件")
        return

    log_files.sort(key=lambda x: x[0], reverse=True)
    latest_log = log_files[0][1]
    log_path = os.path.join(report_dir, latest_log)

    # 提取设备信息
    device_type, sw_version = extract_device_info_from_filename(latest_log)

    # 从日志中读取测试结果
    total, passed, failed = read_summary_from_log(log_path)

    # 构建邮件正文
    status = "全部通过" if failed == 0 else "存在失败"
    summary_text = f"""自动化测试结果汇总（按测试模块统计）：

设备型号：{device_type}
软件版本：{sw_version}

总模块数：{total}
通过（PASS）：{passed}
失败（FAIL）：{failed}

构建状态：{status}

详细日志请查看附件。
"""

    # 创建邮件
    msg = MIMEMultipart()
    msg['From'] = qq_email
    msg['To'] = recipient
    msg['Subject'] = f'[Jenkins] {device_type} {sw_version} | PASS: {passed} / FAIL: {failed}'
    msg.attach(MIMEText(summary_text, 'plain', 'utf-8'))

    # 添加日志附件
    if os.path.exists(log_path):
        with open(log_path, 'rb') as f:
            part = MIMEText(f.read(), 'base64', 'utf-8')
            part.add_header('Content-Disposition', 'attachment', filename=latest_log)
            part.replace_header('Content-Transfer-Encoding', 'base64')
            msg.attach(part)

    # 发送邮件
    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)
        server.login(qq_email, qq_auth_code)
        server.send_message(msg)
        server.quit()
        print("✅ 邮件发送成功！")
    except Exception as e:
        print(f"❌ 邮件发送失败: {e}")


if __name__ == '__main__':
    send_test_summary()