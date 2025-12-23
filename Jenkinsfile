pipeline {
    agent {
        label 'windows'
    }

    environment {
        QQ_EMAIL         = '2466065809@qq.com'
        QQ_AUTH_CODE     = 'tpyxgmecjqrndiif'
        RECIPIENT        = '2466065809@qq.com'
        WORK_ROOT        = "D:\\pytest_jenkins_test"
        REPORT_DIR       = "D:\\pytest_jenkins_test@tmp"
        TIMESTAMP        = "${new Date().format('yyyy-MM-dd_HH-mm-ss', TimeZone.getTimeZone('Asia/Shanghai'))}"
        HTML_REPORT_FILE = "${REPORT_DIR}\\report_${TIMESTAMP}.html"
        LOG_FILE         = "${REPORT_DIR}\\log_${TIMESTAMP}.txt"
    }

    stages {
        stage('Prepare Custom Workspace') {
            steps {
                bat '''
                    @echo off
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
                    cd /d "%WORK_ROOT%"
                    python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple/
                    if exist "requirements.txt" (
                        pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
                    )
                '''
            }
        }

        stage('Run Pytest Tests') {
            steps {
                script {
                    env.TEST_START_TIME = new Date().format('yyyy-MM-dd HH:mm:ss', TimeZone.getTimeZone('Asia/Shanghai'))
                }
                // 使用 PowerShell 同时输出到控制台和文件
                bat """
                    cd /d \"${env.WORK_ROOT}\"
                    powershell -Command ^
                        \"python -m pytest Test_cases -v --tb=short ^
                            --html='${env.HTML_REPORT_FILE}' ^
                            --self-contained-html ^
                            2>&1 | Tee-Object -FilePath '${env.LOG_FILE}'\"
                """
            }
        }
    }

    post {
        always {
            script {
                def endTime = new Date().format('yyyy-MM-dd HH:mm:ss', TimeZone.getTimeZone('Asia/Shanghai'))

                // 归档 HTML 报告（用于邮件）
                if (fileExists(env.HTML_REPORT_FILE)) {
                    archiveArtifacts artifacts: env.HTML_REPORT_FILE, allowEmptyArchive: true
                }

                // 可选：也归档日志（方便在 Jenkins 上查看）
                if (fileExists(env.LOG_FILE)) {
                    archiveArtifacts artifacts: env.LOG_FILE, allowEmptyArchive: true
                }

                // 发送邮件（只附 HTML 报告）
                bat """
                    cd /d "${env.WORK_ROOT}"
                    python send_email.py "${env.TEST_START_TIME}" "${endTime}" "" "" "${env.HTML_REPORT_FILE}"
                """
            }
        }
    }
}