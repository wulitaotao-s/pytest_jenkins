pipeline {
    agent { 
        label 'windows'  
    }

    environment {
        QQ_EMAIL         = '2466065809@qq.com'
        QQ_AUTH_CODE     = 'tpyxgmecjqrndiif'
        RECIPIENT        = '2466065809@qq.com'
        WORK_ROOT        = "D:\\pytest_jenkins_test"   // 自定义工作目录
        REPORT_DIR       = "D:\\pytest_jenkins_test\\Reports"
        VENV_DIR         = "D:\\pytest_jenkins_test\\.venv"
    }

    stages {
        stage('Prepare Custom Workspace') {
            steps {
                // 确保目录存在
                bat '''
                    @echo off
                    echo [INFO] Preparing custom workspace at %WORK_ROOT%
                    mkdir "%WORK_ROOT%" 2>nul
                    exit /b 0
                '''
            }
        }

        stage('Checkout into Custom Directory') {
            steps {
                dir(env.WORK_ROOT) {
                    // 清理旧内容（可选）
                    bat 'rd /s /q . 2>nul || exit /b 0'
                    // 重新拉取代码
                    checkout scm
                }
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
                        echo [FATAL] Python not found in PATH.
                        exit /b 1
                    )

                    echo [INFO] Checking for existing virtual environment at %VENV_DIR%...
                    if exist "%VENV_DIR%" (
                        echo [INFO] Virtual environment already exists. Skipping creation.
                        exit /b 0
                    )

                    echo [INFO] Creating virtual environment at %VENV_DIR%...
                    python -m venv "%VENV_DIR%"
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
                bat '''
                    @echo off
                    call "%VENV_DIR%\\Scripts\\activate.bat"
                    echo [INFO] Upgrading pip...
                    python -m pip install --upgrade pip
                    if %ERRORLEVEL% neq 0 (
                        echo [ERROR] Failed to upgrade pip.
                        exit /b 1
                    )

                    cd /d "%WORK_ROOT%"

                    echo [INFO] Installing dependencies from requirements.txt...
                    if not exist "requirements.txt" (
                        echo [WARN] requirements.txt not found. Skipping.
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

                    env.TEST_OUTPUT_FILE = "D:\\pytest_jenkins_test\\Reports\\pytest_console_${timestamp}.log"
                    env.HTML_REPORT_FILE = "D:\\pytest_jenkins_test\\Reports\\report_${timestamp}.html"

                    bat """
                        @echo off
                        mkdir \"${env.REPORT_DIR}\" 2>nul

                        call \"${env.VENV_DIR}\\Scripts\\activate.bat\"
                        cd /d \"${env.WORK_ROOT}\"

                        echo [INFO] Running pytest...
                        python -m pytest Test_cases -v --tb=short ^
                            --html=\"${env.HTML_REPORT_FILE}\" ^
                            --self-contained-html ^
                            1>\"${env.TEST_OUTPUT_FILE}\" 2>&1

                        if %ERRORLEVEL% neq 0 (
                            echo [WARN] Pytest exited with non-zero code (tests may have failed).
                        )

                        if not exist \"${env.TEST_OUTPUT_FILE}\" (
                            echo [ERROR] Console log not generated.
                            echo [ERROR] Pytest did not generate console log. > \"${env.TEST_OUTPUT_FILE}\"
                        )

                        echo [INFO] Pytest completed.
                        exit /b 0
                    """

                    if (fileExists(env.TEST_OUTPUT_FILE)) {
                        def content = readFile(file: env.TEST_OUTPUT_FILE, encoding: 'UTF-8')
                        echo "=== Pytest Console Log ===\n${content}\n=== End ==="
                    } else {
                        echo "[WARNING] Test output file not found."
                    }
                }
            }
        }

        stage('Send Email Report') {
            steps {
                bat """
                    @echo off
                    cd /d \"${env.WORK_ROOT}\"
                    if not exist \"send_email.py\" (
                        echo [WARN] send_email.py not found. Skipping email.
                        exit /b 0
                    )
                    call \"${env.VENV_DIR}\\Scripts\\activate.bat\"
                    echo [INFO] Sending email report...
                    python send_email.py
                    if %ERRORLEVEL% neq 0 (
                        echo [ERROR] Failed to send email.
                        exit /b 1
                    )
                    echo [INFO] Email sent successfully.
                    exit /b 0
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

        // 可选：清理整个目录（谨慎使用！）
        // cleanup {
        //     bat 'rd /s /q "D:\\pytest_jenkins_test" 2>nul && echo [INFO] Cleaned up D:\\pytest_jenkins_test'
        // }
    }
}