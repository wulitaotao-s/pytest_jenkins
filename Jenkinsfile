pipeline {
    agent any

    environment {
        QQ_EMAIL = '2466065809@qq.com'
        QQ_AUTH_CODE = 'tpyxgmecjqrndiif'
        RECIPIENT = '2466065809@qq.com'
        REPORT_DIR = 'D:\\pytest_jenkins\\report'
        JSON_REPORT = 'D:\\pytest_jenkins\\report\\test_result.json'
        LOG_FILE = 'D:\\pytest_jenkins\\report\\test_run.log'  // 与 run_all_tests.py 一致
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create Report Directory') {
            steps {
                bat 'mkdir "${REPORT_DIR}" 2>nul || exit /b 0'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
                bat 'pip install pytest-json-report'
            }
        }

        stage('Run Tests & Generate Reports') {
            steps {
                // 直接运行主控脚本，它内部会调用 pytest 并生成 log + json
                bat 'python run_all_tests.py'

                // 可选：打印日志末尾便于调试
                bat 'type "${LOG_FILE}" | findstr /C:"测试结束时间"'
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