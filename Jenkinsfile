pipeline {
    agent any

    environment {
        // 报告文件名带时间戳
        REPORT_FILENAME = "test_report_${BUILD_ID}.html"
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
                // 创建报告目录（如果不存在）
                bat 'if not exist "D:\\pytest_jenkins\\report" mkdir "D:\\pytest_jenkins\\report"'

                // 运行 pytest 并生成 HTML 报告
                bat "python -m pytest --html=${env.REPORT_FILENAME} --self-contained-html"

                // 复制报告到固定目录（可选）
                bat "copy ${env.REPORT_FILENAME} D:\\pytest_jenkins\\report\\${env.REPORT_FILENAME}"
            }
        }
    }

    post {
        always {
            script {
                echo "📁 当前工作目录: ${pwd()}"
                echo "📄 期望的报告文件名: ${env.REPORT_FILENAME}"
                echo "📂 本地完整路径: D:\\pytest_jenkins\\report\\${env.REPORT_FILENAME}"

                if (fileExists(env.REPORT_FILENAME)) {
                    echo "✅ 报告文件已生成。文件信息如下："
                    bat "dir /b ${env.REPORT_FILENAME} && dir ${env.REPORT_FILENAME}"

                    // 归档报告（用于 Jenkins UI 查看）
                    archiveArtifacts artifacts: env.REPORT_FILENAME, fingerprint: true
                } else {
                    echo "❌ 报告文件未找到！"
                }
            }
        }

        success {
            script {
                echo "🎉 测试成功，准备发送成功邮件..."
                sendTestReportEmail(
                    "[SUCCESS] Pytest CI 成功 - 构建 #${BUILD_NUMBER}",
                    "所有测试用例执行通过，HTML 测试报告已生成并作为附件发送。"
                )
            }
        }

        failure {
            script {
                echo "💥 测试失败，准备发送失败通知..."
                sendTestReportEmail(
                    "[FAILED] Pytest CI 失败 - 构建 #${BUILD_NUMBER}",
                    "测试执行过程中出现失败，请及时检查日志和报告。"
                )
            }
        }
    }
}

// 邮件发送函数（关键：添加 credentialsId）
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
        attachmentsPattern: env.REPORT_FILENAME,
        credentialsId: 'qq-email'  // ← 关键：指定凭据 ID
    )
    echo "📧 邮件发送指令已调用（使用凭据 ID: qq-email）"
}