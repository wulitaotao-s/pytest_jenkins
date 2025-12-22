pipeline {
    agent { 
        label 'windows'  
    }

    environment {
        QQ_EMAIL         = '2466065809@qq.com'
        QQ_AUTH_CODE     = 'tpyxgmecjqrndiif'
        RECIPIENT        = '2466065809@qq.com'
        WORK_ROOT        = "D:\\pytest_jenkins_test"
        REPORT_DIR       = "D:\\pytest_jenkins_test\\Reports"
        // VENV_DIR 被移除，不再使用
    }

    stages {
        stage('Prepare Custom Workspace') {
            steps {
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
                    bat 'rd /s /q . 2>nul || exit /b 0'
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

        // ❌ 移除 "Create Virtual Environment" stage

        stage('Install Dependencies') {
            steps {
                bat '''
                    @echo off
                    cd /d "%WORK_ROOT%"

                    echo [INFO] Checking Python and pip...
                    where python >nul 2>&1
                    if %ERRORLEVEL% neq 0 (
                        echo [FATAL] 'python' not found in PATH. Please install Python and add to PATH.
                        exit /b 1
                    )

                    python --version
                    pip --version

                    echo [INFO] Upgrading pip...
                    python -m pip install --upgrade pip
                    if %ERRORLEVEL% neq 0 (
                        echo [ERROR] Failed to upgrade pip.
                        exit /b 1
                    )

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
    }
}