pipeline {
    agent { 
        label 'windows'  
    }

    environment {
        QQ_EMAIL = '2466065809@qq.com'
        QQ_AUTH_CODE = 'tpyxgmecjqrndiif'
        RECIPIENT = '2466065809@qq.com'
        REPORT_DIR = "D:\\pytest_jenkins\\Reports"  // Groovy 字符串，双反斜杠
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create Report Directory') {
            steps {
                // 使用 %REPORT_DIR%（Windows 环境变量语法）
                bat 'mkdir "%REPORT_DIR%" 2>nul || exit /b 0'
                // 可选：也创建 workspace/report（如果你需要）
                // bat 'mkdir "%WORKSPACE%\\report" 2>nul || exit /b 0'
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
                    def now = new Date()
                    def timestamp = String.format('%tY-%<tm-%<td_%<tH-%<tM-%<tS', now)

                    // 构造完整路径（注意：这里用双反斜杠或单正斜杠均可）
                    env.TEST_OUTPUT_FILE = "D:\\pytest_jenkins\\Reports\\pytest_console_${timestamp}.log"
                    env.HTML_REPORT_FILE = "D:\\pytest_jenkins\\Reports\\report_${timestamp}.html"

                    // 再次确保目录存在（安全起见）
                    bat 'mkdir "%REPORT_DIR%" 2>nul || exit /b 0'

                    // 运行 pytest
                    bat """
                        python -m pytest Test_cases -v --tb=short ^
                        --html="%HTML_REPORT_FILE%" ^
                        --self-contained-html ^
                        1>"%TEST_OUTPUT_FILE%" 2>&1
                    """

                    // 检查日志是否生成
                    if (!fileExists(env.TEST_OUTPUT_FILE)) {
                        bat "echo [ERROR] Pytest did not generate console log. > \"%TEST_OUTPUT_FILE%\""
                    }

                    // 打印日志到控制台
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
                if (env.TEST_OUTPUTFILE && fileExists(env.TEST_OUTPUT_FILE)) {
                    archiveArtifacts artifacts: env.TEST_OUTPUT_FILE, allowEmptyArchive: true
                }
                if (env.HTML_REPORT_FILE && fileExists(env.HTML_REPORT_FILE)) {
                    archiveArtifacts artifacts: env.HTML_REPORT_FILE, allowEmptyArchive: true
                }
            }
        }
    }
}