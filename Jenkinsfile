pipeline {
    agent { 
        label 'windows'  
    }

    environment {
        QQ_EMAIL = '2466065809@qq.com'
        QQ_AUTH_CODE = 'tpyxgmecjqrndiif'
        RECIPIENT = '2466065809@qq.com'
        REPORT_DIR = "D:\\pytest_jenkins\\Reports"
        VENV_DIR = ".venv"  // 虚拟环境目录（相对于 workspace）
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create Report Directory') {
            steps {
                bat 'mkdir "%REPORT_DIR%" 2>nul || exit /b 0'
            }
        }

        stage('Create Virtual Environment') {
            steps {
                // 创建虚拟环境（如果不存在）
                bat 'if not exist "%VENV_DIR%" python -m venv "%VENV_DIR%"'
            }
        }

        stage('Install Dependencies') {
            steps {
                // 激活虚拟环境并安装依赖
                bat """
                    call "%VENV_DIR%\\Scripts\\activate.bat"
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                """
            }
        }

        stage('Run Pytest Tests') {
            steps {
                script {
                    def now = new Date()
                    def timestamp = String.format('%tY-%<tm-%<td_%<tH-%<tM-%<tS', now)

                    env.TEST_OUTPUT_FILE = "D:\\pytest_jenkins\\Reports\\pytest_console_${timestamp}.log"
                    env.HTML_REPORT_FILE = "D:\\pytest_jenkins\\Reports\\report_${timestamp}.html"

                    bat 'mkdir "%REPORT_DIR%" 2>nul || exit /b 0'

                    // 在虚拟环境中运行 pytest
                    bat """
                        call "%VENV_DIR%\\Scripts\\activate.bat"
                        python -m pytest Test_cases -v --tb=short ^
                        --html="%HTML_REPORT_FILE%" ^
                        --self-contained-html ^
                        1>"%TEST_OUTPUT_FILE%" 2>&1
                    """

                    if (!fileExists(env.TEST_OUTPUT_FILE)) {
                        bat "echo [ERROR] Pytest did not generate console log. > \"%TEST_OUTPUT_FILE%\""
                    }

                    def content = readFile(file: env.TEST_OUTPUT_FILE, encoding: 'UTF-8')
                    echo "=== Pytest Console Log ===\n${content}\n=== End ==="
                }
            }
        }

        stage('Send Email Report') {
            steps {
                // 注意：send_email.py 也应在虚拟环境中运行（如果它依赖某些库）
                bat """
                    call "%VENV_DIR%\\Scripts\\activate.bat"
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

        // 可选：清理虚拟环境（节省磁盘空间）
        // cleanup {
        //     bat 'rd /s /q ".venv" 2>nul || exit /b 0'
        // }
    }
}