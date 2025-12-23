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

        stage('Set Dynamic Variables') {
            steps {
                script {
                    def ts = new Date().format('yyyy-MM-dd_HH-mm-ss', TimeZone.getTimeZone('Asia/Shanghai'))
                    env.TIMESTAMP = ts
                    env.HTML_REPORT_FILE = "${env.REPORT_DIR}\\report_${ts}.html"
                    env.LOG_FILE = "${env.REPORT_DIR}\\log_${ts}.txt"
                    env.TEST_START_TIME = new Date().format('yyyy-MM-dd HH:mm:ss', TimeZone.getTimeZone('Asia/Shanghai'))
                }
            }
        }

        stage('Run Pytest Tests') {
            steps {
                bat """
                    cd /d \"${env.WORK_ROOT}\"
                    powershell -Command "python -m pytest Test_cases -v --tb=short --html='${env.HTML_REPORT_FILE}' --self-contained-html 2>&1 | Tee-Object -FilePath '${env.LOG_FILE}'"
                """
            }
        }
    }

    post {
        always {
            script {
                def endTime = new Date().format('yyyy-MM-dd HH:mm:ss', TimeZone.getTimeZone('Asia/Shanghai'))

                if (fileExists(env.HTML_REPORT_FILE)) {
                    archiveArtifacts artifacts: env.HTML_REPORT_FILE, allowEmptyArchive: true
                }
                if (fileExists(env.LOG_FILE)) {
                    archiveArtifacts artifacts: env.LOG_FILE, allowEmptyArchive: true
                }

                bat """
                    cd /d "${env.WORK_ROOT}"
                    python send_email.py "${env.TEST_START_TIME}" "${endTime}" "" "" "${env.HTML_REPORT_FILE}"
                """
            }
        }
    }
}