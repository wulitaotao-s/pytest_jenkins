pipeline {
    agent {
        label 'windows'
    }

    environment {
        QQ_EMAIL         = '2466065809@qq.com'
        QQ_AUTH_CODE     = 'tpyxgmecjqrndiif'
        RECIPIENT        = '2466065809@qq.com'
        WORK_ROOT        = "D:\\pytest_jenkins_test"
        REPORT_DIR       = "D:\\pytest_jenkins_test@tmp" // 改为 @tmp 目录
        TIMESTAMP        = "${new Date().format('yyyy-MM-dd_HH-mm-ss', TimeZone.getTimeZone('Asia/Shanghai'))}"
        HTML_REPORT_FILE = "${REPORT_DIR}\\report_${TIMESTAMP}.html"
        TEST_OUTPUT_FILE = "${REPORT_DIR}\\pytest_console_${TIMESTAMP}.log"

        // 新增：用于传递测试结果（Jenkins 环境变量）
        TEST_START_TIME  = ""
        TEST_END_TIME    = ""
        PASSED_TESTS     = ""
        FAILED_TESTS     = ""
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
                    bat '''
                        @echo off
                        taskkill /f /im python.exe 2>nul
                        taskkill /f /im pythonw.exe 2>nul
                        rd /s /q . 2>nul || exit /b 0
                    '''
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

                    where python >nul 2>&1
                    if %ERRORLEVEL% neq 0 (
                        echo [FATAL] 'python' not found in PATH.
                        exit /b 1
                    )

                    python --version
                    pip --version

                    python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple/
                    if %ERRORLEVEL% neq 0 (
                        echo [ERROR] Failed to upgrade pip.
                        exit /b 1
                    )

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
                    env.TEST_START_TIME = new Date().format('yyyy-MM-dd HH:mm:ss', TimeZone.getTimeZone('Asia/Shanghai'))
                }
                bat """
                    cd /d \"${env.WORK_ROOT}\"
                    mkdir \"${env.REPORT_DIR}\" 2>nul

                    set PYTHONUNBUFFERED=1
                    python -m pytest Test_cases -v -s ^
                        --tb=short ^
                        --html=\"${env.HTML_REPORT_FILE}\" ^
                        --self-contained-html ^
                        1>\"${env.TEST_OUTPUT_FILE}\" 2>&1
                """
            }
        }
    }

    post {
        always {
            script {
                echo "[INFO] Entering post-build actions..."

                // 记录结束时间
                env.TEST_END_TIME = new Date().format('yyyy-MM-dd HH:mm:ss', TimeZone.getTimeZone('Asia/Shanghai'))

                def passedTests = []
                def failedTests = []

                if (fileExists(env.TEST_OUTPUT_FILE)) {
                    def content = readFile(file: env.TEST_OUTPUT_FILE)
                    def lines = content.split('\n')

                    for (def line : lines) {
                        line = line.trim()
                        if (line =~ /^.*PASSED$/) {
                            def match = (line =~ /^(.+?)\s+PASSED$/)
                            if (match) {
                                passedTests.add(match[0][1].trim())
                            }
                        } else if (line =~ /^.*FAILED$/) {
                            def match = (line =~ /^(.+?)\s+FAILED$/)
                            if (match) {
                                failedTests.add(match[0][1].trim())
                            }
                        } else if (line =~ /^.*ERROR$/) {
                            def match = (line =~ /^(.+?)\s+ERROR$/)
                            if (match) {
                                failedTests.add(match[0][1].trim())
                            }
                        }
                    }
                }

                // 去重并转为字符串
                env.PASSED_TESTS = passedTests.unique().join(', ')
                env.FAILED_TESTS = failedTests.unique().join(', ')

                echo "[SUMMARY] Passed: ${passedTests.size()}, Failed: ${failedTests.size()}"

                // 归档
                if (fileExists(env.HTML_REPORT_FILE)) {
                    archiveArtifacts artifacts: env.HTML_REPORT_FILE, allowEmptyArchive: true
                }
                if (fileExists(env.TEST_OUTPUT_FILE)) {
                    archiveArtifacts artifacts: env.TEST_OUTPUT_FILE, allowEmptyArchive: true
                }

                // ✅ 关键：将环境变量导出到 Windows 环境（供 Python 使用）
                bat """
                    set "TEST_START_TIME=${env.TEST_START_TIME}"
                    set "TEST_END_TIME=${env.TEST_END_TIME}"
                    set "PASSED_TESTS=${env.PASSED_TESTS}"
                    set "FAILED_TESTS=${env.FAILED_TESTS}"
                    cd /d "${env.WORK_ROOT}"
                    python send_email.py
                """
            }
        }
    }
}