pipeline {
    agent any

    environment {
        // 邮件配置（建议后续改用 credentials() 存储密码）
        QQ_EMAIL = '2466065809@qq.com'               
        QQ_AUTH_CODE = 'tpyxgmecjqrndiif'      
        RECIPIENT = '2466065809@qq.com'        

        // 报告配置
        REPORT_NAME = 'pytest-测试报告'
        REPORT_DIR = 'reports'
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
                // Windows bat 中必须用 %VAR%，不能用 ${VAR}
                bat 'if not exist "%REPORT_DIR%" mkdir "%REPORT_DIR%"'
                bat 'python -m pytest --html=%REPORT_NAME% --self-contained-html'
                bat 'copy %REPORT_NAME% %REPORT_DIR%\\%REPORT_NAME%'
            }
        }
    }

    post {
        always {
            script {
                echo '准备通过 Python 发送测试报告邮件...'
            }
            bat 'python send_email.py'
            archiveArtifacts artifacts: "${env.REPORT_DIR}\\${env.REPORT_NAME}", fingerprint: true
        }
    }
}