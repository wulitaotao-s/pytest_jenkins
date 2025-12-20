pipeline {
    agent any

    environment {
        QQ_EMAIL = '2466065809@qq.com'
        QQ_AUTH_CODE = 'tpyxgmecjqrndiif'
        RECIPIENT = '2466065809@qq.com'
        REPORT_DIR = "D:\\pytest_jenkins\\Reports"
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
                bat 'mkdir "%WORKSPACE%\\report" 2>nul || exit /b 0'
                bat 'mkdir "${REPORT_DIR}" 2>nul || exit /b 0'
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
                    // 安全生成时间戳
                    def now = new Date()
                    def timestamp = String.format('%tY-%<tm-%<td_%<tH-%<tM-%<tS', now)
                    env.TEST_OUTPUT_FILE = "${env.REPORT_DIR}\\test_report_${timestamp}.log"

                    // 确保目录存在
                    bat 'mkdir "${REPORT_DIR}" 2>nul || exit /b 0'

                    // 运行测试并保存日志
                    bat "python run_all_tests.py 1>\"${env.TEST_OUTPUT_FILE}\" 2>&1"

                    // 如果日志不存在，创建一个
                    if (!fileExists(env.TEST_OUTPUT_FILE)) {
                        bat "echo [ERROR] Test process crashed or log not generated. > \"${env.TEST_OUTPUT_FILE}\""
                    }

                    // 打印日志到控制台
                    def content = readFile(file: env.TEST_OUTPUT_FILE, encoding: 'UTF-8')
                    echo "=== Test Log ===\n${content}\n=== End ==="
                }
            }
        }

        stage('Send Email Report') {
            steps {
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
                if (env.TEST_OUTPUT_FILE && fileExists(env.TEST_OUTPUT_FILE)) {
                    archiveArtifacts artifacts: env.TEST_OUTPUT_FILE, allowEmptyArchive: true
                }
            }
        }
    }
}