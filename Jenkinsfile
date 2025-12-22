pipeline {
    agent { 
        label 'windows'  
    }

    environment {
        QQ_EMAIL       = '2466065809@qq.com'
        QQ_AUTH_CODE   = 'tpyxgmecjqrndiif'
        RECIPIENT      = '2466065809@qq.com'
        REPORT_DIR     = "D:\\pytest_jenkins\\Reports"
        VENV_DIR       = ".venv"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create Report Directory') {
            steps {
                bat '''
                    @echo off
                    mkdir "%REPORT_DIR%" 2>nul
                    exit /b 0
                '''
            }
        }

        stage('Create Virtual Environment') {
            steps {
                bat '''
                    @echo off
                    echo [INFO] Checking if Python is available...
                    where python >nul 2>&1
                    if %ERRORLEVEL% neq 0 (
                        echo [FATAL] Python not found in PATH. Please install Python and add it to system PATH.
                        exit /b 1
                    )

                    echo [INFO] Checking for existing virtual environment at .venv...
                    if exist ".venv" (
                        echo [INFO] Virtual environment already exists. Skipping creation.
                        exit /b 0
                    )

                    echo [INFO] Creating virtual environment...
                    python -m venv ".venv"
                    if %ERRORLEVEL% neq 0 (
                        echo [FATAL] Failed to create virtual environment.
                        exit /b 1
                    )

                    echo [INFO] Virtual environment created successfully.
                    exit /b 0
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                // 可选：调试用，确认 .venv 存在
                // bat 'dir .venv'

                bat '''
                    @echo off
                    call ".venv\\Scripts\\activate.bat"
                    echo [INFO] Upgrading pip...
                    python -m pip install --upgrade pip
                    if %ERRORLEVEL% neq 0 (
                        echo [ERROR] Failed to upgrade pip.
                        exit /b 1
                    )

                    echo [INFO] Installing dependencies from requirements.txt...
                    if not exist "requirements.txt" (
                        echo [WARN] requirements.txt not found. Skipping dependency installation.
                        exit /b 0
                    )
                    pip install -r requirements.txt
                    if %ERRORLEVEL% neq 0 (
                        echo [ERROR] Failed to install dependencies.
                        exit /b 1
                    )

                    echo [INFO] Dependencies installed successfully.
                    exit /b 0
                '''
            }
        }

        stage('Run Pytest Tests') {
            steps {
                script {
                    def now = new Date()
                    def timestamp = String.format('%tY-%<tm-%<td_%<tH-%<tM-%<tS', now)

                    env.TEST_OUTPUT_FILE = "D:\\pytest_jenkins\\Reports\\pytest_console_${timestamp}.log"
                    env.HTML_REPORT_FILE = "D:\\pytest_jenkins\\Reports\\report_${timestamp}.html"

                    bat '''
                        @echo off
                        mkdir "%REPORT_DIR%" 2>nul
                        call ".venv\\Scripts\\activate.bat"
                        echo [INFO] Running pytest...
                        python -m pytest Test_cases -v --tb=short ^
                            --html="%HTML_REPORT_FILE%" ^
                            --self-contained-html ^
                            1>"%TEST_OUTPUT_FILE%" 2>&1

                        if %ERRORLEVEL% neq 0 (
                            echo [WARN] Pytest exited with non-zero code (tests may have failed).
                            REM We do NOT fail the build here unless you want to.
                        )

                        if not exist "%TEST_OUTPUT_FILE%" (
                            echo [ERROR] Console log file was not generated.
                            echo [ERROR] Pytest did not generate console log. > "%TEST_OUTPUT_FILE%"
                        )

                        echo [INFO] Pytest completed.
                        exit /b 0
                    '''

                    // 打印日志到 Jenkins 控制台
                    if (fileExists(env.TEST_OUTPUT_FILE)) {
                        def content = readFile(file: env.TEST_OUTPUT_FILE, encoding: 'UTF-8')
                        echo "=== Pytest Console Log ===\n${content}\n=== End ==="
                    } else {
                        echo "[WARNING] Test output file not found for display."
                    }
                }
            }
        }

        stage('Send Email Report') {
            steps {
                bat '''
                    @echo off
                    if not exist "send_email.py" (
                        echo [WARN] send_email.py not found. Skipping email.
                        exit /b 0
                    )
                    call ".venv\\Scripts\\activate.bat"
                    echo [INFO] Sending email report...
                    python send_email.py
                    if %ERRORLEVEL% neq 0 (
                        echo [ERROR] Failed to send email.
                        exit /b 1
                    )
                    echo [INFO] Email sent successfully.
                    exit /b 0
                '''
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

        // 可选：清理虚拟环境（节省空间）
        // cleanup {
        //     bat 'rd /s /q ".venv" 2>nul && echo [INFO] Cleaned up .venv || echo [INFO] No .venv to clean'
        // }
    }
}