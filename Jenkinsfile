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
                powershell '''
                    $timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
                    $logFile = "D:\\pytest_jenkins\\report\\${timestamp}.log"
                    $jsonReport = "D:\\pytest_jenkins\\report\\test_result.json"

                    pytest -v -s --json-report --json-report-file="$jsonReport" Test_cases/test_device_info.py | Out-File -FilePath $logFile -Encoding UTF8

                    Write-Host "测试完成，日志已保存至: $logFile"
                '''
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