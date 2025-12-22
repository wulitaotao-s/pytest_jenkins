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
                    python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple/
                    if %ERRORLEVEL% neq 0 (
                        echo [ERROR] Failed to upgrade pip.
                        exit /b 1
                    )

                    echo [INFO] Installing dependencies from requirements.txt...
                    if not exist "requirements.txt" (
                        echo [WARN] requirements.txt not found. Skipping.
                        exit /b 0
                    )
                    pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
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
                    env.HTML_REPORT_FILE = "D:\\pytest_jenkins_test\\Reports\\report_${timestamp}.html"
                    env.TEST_OUTPUT_FILE = "D:\\pytest_jenkins_test\\Reports\\pytest_console_${timestamp}.log"

                    bat """
                        cd /d \"${env.WORK_ROOT}\"
                        mkdir \"${env.REPORT_DIR}\" 2>nul

                        echo [INFO] Running pytest with real-time logging...

                        set PYTHONUNBUFFERED=1
                        python -m pytest Test_cases -v -s ^
                            --tb=short ^
                            --html=\"${env.HTML_REPORT_FILE}\" ^
                            --self-contained-html ^
                            1>\"${env.TEST_OUTPUT_FILE}\" 2>&1
                    """

                    // 可选：实时打印到 Jenkins 控制台（用于调试）
                    if (fileExists(env.TEST_OUTPUT_FILE)) {
                        def lines = readFile(file: env.TEST_OUTPUT_FILE).split('\n')
                        for (line in lines) {
                            if (line.contains('[TEST LOG]')) {
                                echo line
                            }
                        }
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