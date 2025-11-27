pipeline {
    agent any

    environment {
        // 🔑 替换为你的真实信息（或使用 credentials）
        QQ_EMAIL = '2466065809@qq.com'
        QQ_AUTH_CODE = 'tpyxgmecjqrndiif'  
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

                // 调用独立的 Python 脚本（关键！）
                bat 'python send_email.py'
            }

            archiveArtifacts artifacts: 'test_report_22.html', fingerprint: true
        }
    }
}