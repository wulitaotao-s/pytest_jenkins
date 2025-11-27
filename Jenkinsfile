pipeline {
    agent any

    environment {
        // 🔑 替换为你的 QQ 邮箱和授权码（建议用 Jenkins Credentials 管理）
        QQ_EMAIL = 'your_qq_email@qq.com'       // ←←← 改这里
        QQ_AUTH_CODE = 'your_authorization_code' // ←←← 改这里（QQ邮箱授权码）
        RECIPIENT = '2466065809@qq.com'
        REPORT_NAME = 'test_report_22.html'
        REPORT_DIR = 'D:\\pytest_jenkins\\report'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests & Generate HTML Report') {
            steps {
                bat 'if not exist "${REPORT_DIR}" mkdir "${REPORT_DIR}"'
                bat 'python -m pytest --html=${REPORT_NAME} --self-contained-html'
                bat 'copy ${REPORT_NAME} ${REPORT_DIR}\\${REPORT_NAME}'
            }
        }
    }

    post {
        always {
            script {
                echo "✅ 准备通过 Python 发送测试报告邮件..."

                // 使用 bat 执行内联 Python 脚本（Windows 兼容）
                bat '''
                    python -c "
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# 从环境变量获取配置
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

# 添加 HTML 内容
msg.attach(MIMEText(html_content, 'html', 'utf-8'))

# 发送邮件
try:
    server = smtplib.SMTP_SSL('smtp.qq.com', 465)
    server.login(qq_email, qq_auth_code)
    server.send_message(msg)
    server.quit()
    print('✅ 邮件发送成功！收件人: ' + recipient)
except Exception as e:
    print('❌ 邮件发送失败:', str(e))
    exit(1)
"
                '''
            }

            // 归档报告（可选）
            archiveArtifacts artifacts: 'test_report_22.html', fingerprint: true
        }
    }
}