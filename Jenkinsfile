pipeline {
    agent any

    environment {
        // 改为相对路径：基于 Jenkins 工作区
        REPORT_DIR   = "${WORKSPACE}\\report"
        JSON_REPORT  = "${WORKSPACE}\\report\\test_result.json"
        LOG_FILE     = "${WORKSPACE}\\report\\test_run.log"

        // 邮件配置（保持不变）
        QQ_EMAIL     = '2466065809@qq.com'
        QQ_AUTH_CODE = 'tpyxgmecjqrndiif'
        RECIPIENT    = '2466065809@qq.com'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create Report Directory') {
            steps {
                // 创建目录，即使存在也不报错
                bat 'mkdir "%REPORT_DIR%" 2>nul || exit /b 0'
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
                // 主测试脚本（它内部调用 pytest）
                bat 'python run_all_tests.py'

                // 安全地打印日志末尾（不因 findstr 失败而中断）
                bat '''
                    type "%LOG_FILE%" | findstr /C:"测试结束时间" >nul 2>&1 || (
                        echo (未找到"测试结束时间"，但继续执行)
                    )
                '''
            }
        }
    }

    post {
        always {
            script {
                echo '正在解析测试结果并发送邮件...'
            }
            // 发送邮件（假设 send_email.py 能处理成功/失败）
            bat 'python send_email.py'
        }
    }
}