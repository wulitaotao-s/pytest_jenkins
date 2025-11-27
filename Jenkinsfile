pipeline {
    agent any

    environment {
        QQ_EMAIL = '2466065809@qq.com'                
        QQ_AUTH_CODE = 'tpyxgmecjqrndiif'
        RECIPIENT = '2466065809@qq.com'
        JSON_REPORT = 'report.json'             
    }

    stages {
        stage('Checkout') {
            steps { checkout scm }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests & Generate JSON Report') {
            steps {
                // 生成 JSON 报告（不生成 HTML）
                bat 'python -m pytest --json-report --json-report-file=%JSON_REPORT%'
            }
        }
    }

    post {
        always {
            script { echo '正在解析测试结果并发送邮件...' }
            bat 'python send_email.py'
        }
    }
}