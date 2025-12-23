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
        // 注意：TIMESTAMP 在每个 run 中只计算一次，但 post 阶段仍可访问
        TIMESTAMP        = "${new Date().format('yyyy-MM-dd_HH-mm-ss', TimeZone.getTimeZone('Asia/Shanghai'))}"
        HTML_REPORT_FILE = "D:\\pytest_jenkins_test\\Reports\\report_${TIMESTAMP}.html"
        TEST_OUTPUT_FILE = "D:\\pytest_jenkins_test\\Reports\\pytest_console_${TIMESTAMP}.log"
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
                // 先清理 Python 进程（忽略退出码）
                bat '''
                    @echo off
                    taskkill /f /im python.exe 2>nul
                    taskkill /f /im pythonw.exe 2>nul
                    exit /b 0
                '''

                // 再清理目录
                bat '''
                    @echo off
                    rd /s /q . 2>nul || exit /b 0
                '''

                // 最后 checkout
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

        stage('Install Dependencies') {
            steps {
                bat '''
                    @echo off
                    cd /d "%WORK_ROOT%"

                    echo [INFO] Checking Python and pip...
                    where python >nul 2>&1
                    if %ERRORLEVEL% neq 0 (
                        echo [FATAL] 'python' not found in PATH.
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

                script {
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
    }

    post {
        always {
            script {
                echo "[INFO] Entering post-build actions..."

                // 归档报告和日志
                if (fileExists(env.HTML_REPORT_FILE)) {
                    archiveArtifacts artifacts: env.HTML_REPORT_FILE, allowEmptyArchive: true
                }
                if (fileExists(env.TEST_OUTPUT_FILE)) {
                    archiveArtifacts artifacts: env.TEST_OUTPUT_FILE, allowEmptyArchive: true
                }

                // 发送邮件（无论成功/失败）
                if (fileExists("${env.WORK_ROOT}/send_email.py")) {
                    echo "[INFO] send_email.py found. Sending email report..."
                    bat "cd /d \"${env.WORK_ROOT}\" && python send_email.py"
                    echo "[INFO] Email sending completed."
                } else {
                    echo "[WARN] send_email.py not found at ${env.WORK_ROOT}. Skipping email."
                }
            }
        }
    }
}