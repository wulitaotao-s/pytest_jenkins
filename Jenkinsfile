pipeline {
    agent any

    environment {
        QQ_EMAIL = '2466065809@qq.com'
        QQ_AUTH_CODE = 'tpyxgmecjqrndiif'
        RECIPIENT = '2466065809@qq.com'
        REPORT_ROOT = "${WORKSPACE}\\report"
        DEVICE_TYPE = "Unknown"
        SOFTWARE_VERSION = "Unknown"
        TEST_OUTPUT_FILE = ""
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create Report Directory') {
            steps {
                bat 'mkdir "%REPORT_ROOT%" 2>nul || exit /b 0'
                bat 'mkdir "D:\\pytest_jenkins\\Reports" 2>nul || exit /b 0'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
                bat 'pip install pytest selenium beautifulsoup4'
            }
        }

        stage('Get Device Info') {
            steps {
                script {
                    def infoResult = bat(
                        script: 'python get_info.py',
                        returnStdout: true
                    ).trim()

                    def deviceMatch = infoResult =~ /Device Type:\s*(.+)/
                    def versionMatch = infoResult =~ /Software Version:\s*(.+)/

                    env.DEVICE_TYPE = deviceMatch ? deviceMatch[0][1].trim() : "Unknown"
                    env.SOFTWARE_VERSION = versionMatch ? versionMatch[0][1].trim() : "Unknown"

                    def timestamp = new Date().format('yyyy-MM-dd_HH-mm-ss', TimeZone.getTimeZone('Asia/Shanghai'))
                    env.TEST_OUTPUT_FILE = "D:\\pytest_jenkins\\Reports\\${timestamp} ${env.DEVICE_TYPE} ${env.SOFTWARE_VERSION}.log"

                    echo "Device Type: ${env.DEVICE_TYPE}"
                    echo "Software Version: ${env.SOFTWARE_VERSION}"
                    echo "Log file: ${env.TEST_OUTPUT_FILE}"
                }
            }
        }

        stage('Run All Tests') {
            steps {
                script {
                    bat 'mkdir "D:\\pytest_jenkins\\Reports" 2>nul || exit /b 0'
                    bat "python run_all_tests.py 1>\"${env.TEST_OUTPUT_FILE}\" 2>&1"

                    def content = readFile(file: env.TEST_OUTPUT_FILE, encoding: 'UTF-8')
                    echo content
                }
            }
        }

        stage('Send Email Report') {
            steps {
                bat 'python send_email.py'
            }
        }
    }

    post {
        always {
            script {
                if (env.TEST_OUTPUT_FILE && fileExists(env.TEST_OUTPUT_FILE)) {
                    archiveArtifacts artifacts: env.TEST_OUTPUT_FILE, allowEmptyArchive: true
                }
            }
        }
    }
}