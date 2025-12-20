pipeline {
    agent any

    environment {
        QQ_EMAIL       = '2466065809@qq.com'
        QQ_AUTH_CODE   = 'tpyxgmecjqrndiif'
        RECIPIENT      = '2466065809@qq.com'
        REPORT_ROOT    = "${WORKSPACE}\\report"
        DEVICE_TYPE    = "Unknown"
        SOFTWARE_VERSION = "Unknown"
        TEST_OUTPUT_FILE = "${WORKSPACE}\\test_output.log"
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
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
                bat 'pip install pytest selenium'
            }
        }

        stage('Get Device Info') {
            steps {
                script {
                    def infoResult = bat(
                        script: 'python get_info.py',
                        returnStdout: true
                    ).trim()

                    // 解析 Device Type 和 Software Version
                    def deviceMatch = infoResult =~ /Device Type:\s*(.+)/
                    def versionMatch = infoResult =~ /Software Version:\s*(.+)/

                    env.DEVICE_TYPE = deviceMatch ? deviceMatch[0][1].trim() : "Unknown"
                    env.SOFTWARE_VERSION = versionMatch ? versionMatch[0][1].trim() : "Unknown"

                    echo "Device Type: ${env.DEVICE_TYPE}"
                    echo "Software Version: ${env.SOFTWARE_VERSION}"
                }
            }
        }

        stage('Run All Tests') {
            steps {
                script {
                    bat "python run_all_tests.py > \"${env.TEST_OUTPUT_FILE}\" 2>&1"
                }
            }
        }

        stage('Send Email Report') {
            steps {
                bat 'python send_email.py'
            }
        }
    }
}