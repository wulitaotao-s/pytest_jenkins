pipeline {
    agent any

    environment {
        // 使用 PowerShell 获取当前时间（Windows 安全兼容）
        REPORT_TIME = powershell(returnStdout: true, script: "Get-Date -Format 'yyyyMMdd_HHmmss'").trim()
        REPORT_FILENAME = "test_report_${REPORT_TIME}.html"
        LOCAL_REPORT_DIR = "D:\\pytest_jenkins\\report"
        FULL_REPORT_PATH = "${LOCAL_REPORT_DIR}\\${REPORT_FILENAME}"
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
                // 创建本地报告目录（如果不存在）
                bat 'if not exist "${LOCAL_REPORT_DIR}" mkdir "${LOCAL_REPORT_DIR}"'

                // 运行 pytest 并生成自包含 HTML 报告
                bat "python -m pytest --html=${REPORT_FILENAME} --self-contained-html"

                // 复制报告到指定本地路径（可选，用于本地存档）
                bat "copy ${REPORT_FILENAME} ${FULL_REPORT_PATH}"

                // 调试：确认文件已生成
                script {
                    echo "🔍 报告生成完成。当前工作目录文件列表："
                    bat 'dir /b *.html'
                }
            }
        }
    }

    post {
        always {
            // 归档报告，可在 Jenkins 构建页面下载
            archiveArtifacts artifacts: "${env.REPORT_FILENAME}", fingerprint: true

            // 📌 关键诊断步骤：检查报告是否存在，打印路径
            script {
                echo "📂 当前工作目录: ${pwd()}"
                echo "📄 期望的报告文件名: ${env.REPORT_FILENAME}"
                echo "💾 本地完整路径: ${env.FULL_REPORT_PATH}"

                def reportExists = fileExists("${env.REPORT_FILENAME}")
                if (reportExists) {
                    def size = sh(script: "ls -l ${env.REPORT_FILENAME} | awk '{print \$5}'", returnStdout: true).trim()
                    // 在 Windows 上用 bat 替代
                    if (isUnix()) {
                        echo "✅ 报告文件存在，大小: ${size} 字节"
                    } else {
                        bat "echo 文件大小（字节）: && for %I in (${env.REPORT_FILENAME}) do @echo %~zI"
                    }
                } else {
                    echo "❌ 警告：报告文件 ${env.REPORT_FILENAME} 不存在！邮件将无附件。"
                }
            }
        }

        success {
            script {
                echo "✅ 测试成功！准备发送成功邮件..."
                sendTestReportEmail("[SUCCESS] Pytest Report - Build #${BUILD_NUMBER}", "🎉 自动化测试成功！")
            }
        }

        failure {
            script {
                echo "❌ 测试失败！但仍尝试发送失败邮件..."
                sendTestReportEmail("[FAILED] Pytest Report - Build #${BUILD_NUMBER}", "⚠️ 自动化测试失败！")
            }
        }
    }
}

// 🔧 封装邮件发送逻辑（便于统一处理异常和日志）
def sendTestReportEmail(String subject, String headline) {
    try {
        emailext(
            subject: subject,
            body: """
                <h2>${headline}</h2>
                <p><strong>项目：</strong> pytest_jenkins</p>
                <p><strong>构建号：</strong> #${BUILD_NUMBER}</p>
                <p><strong>构建状态：</strong> ${currentBuild.result ?: 'UNKNOWN'}</p>
                <p><strong>测试完成时间：</strong> ${env.REPORT_TIME}</p>
                <p>详细测试结果请查看附件中的 HTML 报告。</p>
                <hr>
                <small>本邮件由 Jenkins 自动发送 | <a href="${BUILD_URL}">查看构建</a></small>
            """,
            mimeType: 'text/html',
            to: '2466065809@qq.com',
            attachmentsPattern: env.REPORT_FILENAME
        )
        echo "📧 邮件发送指令已成功调用（注意：SMTP 成功需查系统日志）"
    } catch (Exception e) {
        echo "🔥 邮件发送阶段抛出异常: ${e.class.name}: ${e.message}"
        echo "堆栈信息: ${e.stackTrace.join('\n')}"
    }
}