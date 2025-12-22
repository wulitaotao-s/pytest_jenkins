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
        // 使用 BUILD_ID 或自定义时间戳作为唯一标识
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

                // 实时打印带 [TEST LOG] 的行（可选）
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

        stage('Send Email Report') {
            when {
                expression { currentBuild.result != 'SUCCESS' || currentBuild.result == null }
            }
            steps {
                script {
                    def result = bat returnStatus: true, script: """
                        cd /d "${env.WORK_ROOT}"
                        if not exist "send_email.py" (
                            echo [WARN] send_email.py not found. Skipping email.
                            exit /b 0
                        )
                        echo [INFO] Sending email report...
                        python send_email.py
                        exit /b 0
                    """

                    if (result == 0) {
                        echo "[INFO] Email sent successfully."
                    } else {
                        echo "[ERROR] Failed to send email."
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                // 使用 environment 中定义的全局路径
                def htmlFile = env.HTML_REPORT_FILE
                def logFile  = env.TEST_OUTPUT_FILE

                if (fileExists(htmlFile)) {
                    archiveArtifacts artifacts: htmlFile, allowEmptyArchive: true
                }
                if (fileExists(logFile)) {
                    archiveArtifacts artifacts: logFile, allowEmptyArchive: true
                }
            }
        }
    }
}