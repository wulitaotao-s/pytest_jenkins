pipeline {
    agent any

    environment {
        QQ_EMAIL = '2466065809@qq.com'
        QQ_AUTH_CODE = 'tpyxgmecjqrndiif'
        RECIPIENT = '2466065809@qq.com'
        REPORT_DIR = "D:\\pytest_jenkins\\Reports"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create Report Directory') {
            steps {
                bat 'mkdir "%WORKSPACE%\\report" 2>nul || exit /b 0'
                bat 'mkdir "${REPORT_DIR}" 2>nul || exit /b 0'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run Pytest Tests') {
            steps {
                script {
                    // 生成时间戳
                    def now = new Date()
                    def timestamp = String.format('%tY-%<tm-%<td_%<tH-%<tM-%<tS', now)

                    env.TEST_OUTPUT_FILE = "${env.REPORT_DIR}\\pytest_console_${timestamp}.log"
                    env.HTML_REPORT_FILE = "${env.REPORT_DIR}\\report_${timestamp}.html"

                    // 确保目录存在
                    bat 'mkdir "${REPORT_DIR}" 2>nul || exit /b 0'

                    // 直接运行 pytest，输出到日志，并生成 HTML 报告
                    bat """
                        python -m pytest Test_cases -v --tb=short ^
                        --html="${HTML_REPORT_FILE}" ^
                        --self-contained-html ^
                        1>"${TEST_OUTPUT_FILE}" 2>&1
                    """

                    // 如果日志不存在，创建占位文件
                    if (!fileExists(env.TEST_OUTPUT_FILE)) {
                        bat "echo [ERROR] Pytest did not generate console log. > \"${env.TEST_OUTPUT_FILE}\""
                    }

                    // 打印日志到 Jenkins 控制台
                    def content = readFile(file: env.TEST_OUTPUT_FILE, encoding: 'UTF-8')
                    echo "=== Pytest Console Log ===\n${content}\n=== End ==="
                }
            }
        }

        stage('Send Email Report') {
            steps {
                bat """
                    python send_email.py
                """
            }
        }
    }

    post {
        always {
            script {
                if (env.TEST_OUTPUT_FILE && fileExists(env.TEST_OUTPUT_FILE)) {
                    archiveArtifacts artifacts: env.TEST_OUTPUT_FILE, allowEmptyArchive: true
                }
                if (env.HTML_REPORT_FILE && fileExists(env.HTML_REPORT_FILE)) {
                    archiveArtifacts artifacts: env.HTML_REPORT_FILE, allowEmptyArchive: true
                }
            }
        }
    }
}