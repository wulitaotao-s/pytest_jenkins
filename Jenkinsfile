pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                bat 'python -m pip install --upgrade pip'
                bat 'pip install -r requirements.txt'
            }
        }

        stage('Run Tests') {
            steps {
                bat 'python -m pytest'
            }
            post {
                always {
                    // JUnit 报告（确保 pytest 输出 XML）
                    junit '**/test-reports/*.xml'
                }
            }
        }
    }

    post {
        success {
            echo '✅ All tests passed!'
        }
        failure {
            echo '❌ Tests failed!'
        }
    }
}