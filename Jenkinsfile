pipeline {
    agent any

    environment {
        QQ_EMAIL = '2466065809@qq.com'                
        QQ_AUTH_CODE = 'tpyxgmecjqrndiif'
        RECIPIENT = '2466065809@qq.com'
        REPORT_DIR = 'D:\\pytest_jenkins\\report'
        JSON_REPORT = 'D:\\pytest_jenkins\\report\\test_result.json'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create Report Directory') {
            steps {
                bat 'mkdir "${env.REPORT_DIR}" 2>nul || exit /b 0'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests & Generate JSON Report') {
            steps {
                bat 'python -m pytest --json-report --json-report-file="${env.JSON_REPORT}"'
            }
        }
    }

    post {
        always {
            script {
                echo '正在解析测试结果并发送邮件...'
            }
            bat 'python send_email.py'
        }
    }
}