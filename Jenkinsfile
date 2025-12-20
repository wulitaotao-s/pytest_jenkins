pipeline {
    agent any

    environment {
        QQ_EMAIL = '2466065809@qq.com'
        QQ_AUTH_CODE = 'tpyxgmecjqrndiif'
        RECIPIENT = '2466065809@qq.com'
        REPORT_ROOT = "${WORKSPACE}\\report"
        TEST_OUTPUT_FILE = ""
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
                bat 'mkdir "D:\\pytest_jenkins\\Reports" 2>nul || exit /b 0'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
                bat 'pip install pytest selenium beautifulsoup4'
            }
        }

        stage('Run All Tests') {
            steps {
                script {
                    // 使用时间戳生成日志文件名，不依赖设备信息
                    def timestamp = new Date().format('yyyy-MM-dd_HH-mm-ss', TimeZone.getTimeZone('Asia/Shanghai'))
                    env.TEST_OUTPUT_FILE = "D:\\pytest_jenkins\\Reports\\test_report_${timestamp}.log"

                    // 确保目录存在
                    bat 'mkdir "D:\\pytest_jenkins\\Reports" 2>nul || exit /b 0'

                    // 运行测试并重定向输出到日志文件
                    bat "python run_all_tests.py 1>\"${env.TEST_OUTPUT_FILE}\" 2>&1"

                    // 安全读取日志内容（用于 Jenkins 控制台显示）
                    if (fileExists(env.TEST_OUTPUT_FILE)) {
                        def content = readFile(file: env.TEST_OUTPUT_FILE, encoding: 'UTF-8')
                        echo "=== Test Log ===\n${content}\n=== End of Log ==="
                    } else {
                        echo "Warning: Log file not found at ${env.TEST_OUTPUT_FILE}"
                        // 创建占位日志，确保 send_email.py 不崩溃
                        bat "echo [ERROR] Test execution failed or log was not generated. > \"${env.TEST_OUTPUT_FILE}\""
                    }
                }
            }
        }

        stage('Send Email Report') {
            steps {
                // 将日志路径传给 send_email.py（通过环境变量或直接读固定目录）
                bat """
                    set TEST_OUTPUT_FILE=${env.TEST_OUTPUT_FILE}
                    python send_email.py
                """
            }
        }
    }

    post {
        always {
            script {
                // 归档日志（如果存在）
                if (env.TEST_OUTPUT_FILE && fileExists(env.TEST_OUTPUT_FILE)) {
                    archiveArtifacts artifacts: env.TEST_OUTPUT_FILE, allowEmptyArchive: true
                }
            }
        }
    }
}