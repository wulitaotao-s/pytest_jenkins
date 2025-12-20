pipeline {
    agent any

    environment {
        // 邮件配置（使用凭据，不硬编码密码！）
        QQ_EMAIL     = '2466065809@qq.com'
        QQ_AUTH_CODE =   'tpyxgmecjqrndiif'
        RECIPIENT    = '2466065809@qq.com'

        // 日志根目录（可选：使用工作区或固定盘符）
        REPORT_ROOT  = "${WORKSPACE}\\report"  // 或保留 D:\\pytest_jenkins\\Reports
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create Report Directory') {
            steps {
                bat 'mkdir "%REPORT_ROOT%" 2>nul || exit /b 0'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
                bat 'pip install pytest'
                // 不需要 pytest-json-report（除非你用它）
            }
        }

        stage('Run Tests and Send Email') {
            steps {
                // 只调用一个脚本
                bat 'python run_all_tests.py'
            }
        }
    }
}