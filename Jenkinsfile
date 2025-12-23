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
        TIMESTAMP        = "${new Date().format('yyyy-MM-dd_HH-mm-ss', TimeZone.getTimeZone('Asia/Shanghai'))}"
        HTML_REPORT_FILE = "D:\\pytest_jenkins_test\\Reports\\report_${TIMESTAMP}.html"
        TEST_OUTPUT_FILE = "D:\\pytest_jenkins_test\\Reports\\pytest_console_${TIMESTAMP}.log"

        // 新增：用于传递测试结果
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
                    // 记录测试开始时间（Jenkins 时间）
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

                // 记录测试结束时间
                env.TEST_END_TIME = new Date().format('yyyy-MM-dd HH:mm:ss', TimeZone.getTimeZone('Asia/Shanghai'))

                // 初始化列表
                def passedTests = []
                def failedTests = []

                // 从 pytest 日志中提取测试结果
                if (fileExists(env.TEST_OUTPUT_FILE)) {
                    def content = readFile(file: env.TEST_OUTPUT_FILE)
                    def lines = content.split('\n')

                    for (def line : lines) {
                        line = line.trim()
                        // 匹配通过的用例：如 "Test_cases/test_xxx.py::test_yyy PASSED"
                        if (line =~ /^.*PASSED$/) {
                            def match = (line =~ /^(.+?)\s+PASSED$/)
                            if (match) {
                                def testId = match[0][1].trim()
                                passedTests.add(testId)
                            }
                        }
                        // 匹配失败/错误的用例
                        else if (line =~ /^.*FAILED$/) {
                            def match = (line =~ /^(.+?)\s+FAILED$/)
                            if (match) {
                                def testId = match[0][1].trim()
                                failedTests.add(testId)
                            }
                        }
                        else if (line =~ /^.*ERROR$/) {
                            def match = (line =~ /^(.+?)\s+ERROR$/)
                            if (match) {
                                def testId = match[0][1].trim()
                                failedTests.add(testId)
                            }
                        }
                    }
                }

                // 去重（防止重复记录）
                passedTests = passedTests.unique()
                failedTests = failedTests.unique()

                // 转为逗号分隔字符串（供 send_email.py 使用）
                env.PASSED_TESTS = passedTests.join(', ')
                env.FAILED_TESTS = failedTests.join(', ')

                echo "[SUMMARY] Passed: ${passedTests.size()}, Failed: ${failedTests.size()}"

                // 归档报告和日志
                if (fileExists(env.HTML_REPORT_FILE)) {
                    archiveArtifacts artifacts: env.HTML_REPORT_FILE, allowEmptyArchive: true
                }
                if (fileExists(env.TEST_OUTPUT_FILE)) {
                    archiveArtifacts artifacts: env.TEST_OUTPUT_FILE, allowEmptyArchive: true
                }

                // 发送邮件
                if (fileExists("${env.WORK_ROOT}/send_email.py")) {
                    echo "[INFO] Sending email with test summary..."
                    bat "cd /d \"${env.WORK_ROOT}\" && python send_email.py"
                } else {
                    echo "[WARN] send_email.py not found. Skipping email."
                }
            }
        }
    }
}