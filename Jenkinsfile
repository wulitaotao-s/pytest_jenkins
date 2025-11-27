pipeline {
    agent any

    environment {
        // 使用时间戳生成唯一报告文件名
        REPORT_TIMESTAMP = "${new Date().format('yyyyMMdd_HHmmss')}"
        REPORT_FILENAME  = "test_report_${env.REPORT_TIMESTAMP}.html"
        LOCAL_REPORT_DIR = "D:\\pytest_jenkins\\report"
        FULL_REPORT_PATH = "${env.LOCAL_REPORT_DIR}\\${env.REPORT_FILENAME}"
    }

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

        stage('Run Tests & Generate HTML Report') {
            steps {
                // 确保本地报告目录存在
                bat 'if not exist "%LOCAL_REPORT_DIR%" mkdir "%LOCAL_REPORT_DIR%"'

                // 运行 pytest 并生成自包含 HTML 报告
                bat "python -m pytest --html=${env.REPORT_FILENAME} --self-contained-html"

                // 复制报告到指定目录（用于归档或外部访问）
                bat "copy ${env.REPORT_FILENAME} ${env.FULL_REPORT_PATH}"
            }
        }
    }

    post {
        always {
            // 归档生成的 HTML 报告（可在 Jenkins UI 查看）
            archiveArtifacts artifacts: "${env.REPORT_FILENAME}", fingerprint: true

            script {
                echo "📂 当前工作目录: ${pwd()}"
                echo "📄 期望的报告文件名: ${env.REPORT_FILENAME}"
                echo "💾 本地完整路径: ${env.FULL_REPORT_PATH}"

                if (fileExists("${env.REPORT_FILENAME}")) {
                    echo "✅ 报告文件已生成。文件信息如下："
                    // 在 Windows 上显示文件详细信息（含大小）
                    bat "dir /b ${env.REPORT_FILENAME} && dir ${env.REPORT_FILENAME}"
                } else {
                    echo "❌ 警告：报告文件 ${env.REPORT_FILENAME} 不存在！"
                }
            }
        }

        success {
            script {
                echo "🎉 测试成功！准备发送成功邮件..."
                sendTestReportEmail("[SUCCESS] Pytest Report - Build #${BUILD_NUMBER}", "✅ 自动化测试全部通过！")
            }
        }

        failure {
            script {
                echo "⚠️ 测试失败或构建异常！但仍尝试发送失败邮件..."
                sendTestReportEmail("[FAILED] Pytest Report - Build #${BUILD_NUMBER}", "❌ 自动化测试未通过或构建出错！")
            }
        }
    }
}

// 邮件发送函数（可复用）
def sendTestReportEmail(subject, body) {
    emailext (
        subject: subject,
        body: """
${body}

构建编号: #${BUILD_NUMBER}
构建地址: ${BUILD_URL}
报告文件: ${env.REPORT_FILENAME}

请及时查看测试结果。
        """.stripIndent(),
        to: '2466065809@qq.com',
        attachmentsPattern: env.REPORT_FILENAME
    )
    echo "📧 邮件发送指令已调用（请检查 SMTP 日志确认是否成功）"
}