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

                // 复制报告到指定本地路径
                bat "copy ${REPORT_FILENAME} ${FULL_REPORT_PATH}"
            }
        }
    }

    post {
        always {
            // 归档报告，可在 Jenkins 构建页面下载
            archiveArtifacts artifacts: "${env.REPORT_FILENAME}", fingerprint: true
        }

        success {
            echo "✅ 测试成功！报告已保存至: ${env.FULL_REPORT_PATH}"
            emailext (
                subject: "[SUCCESS] Pytest Report - Build #${BUILD_NUMBER}",
                body: """
                <h2>🎉 自动化测试成功！</h2>
                <p><strong>项目：</strong> pytest_jenkins</p>
                <p><strong>构建号：</strong> #${BUILD_NUMBER}</p>
                <p><strong>测试完成时间：</strong> ${env.REPORT_TIME}</p>
                <p>详细测试结果请查看附件中的 HTML 报告。</p>
                <hr>
                <small>本邮件由 Jenkins 自动发送 | ${BUILD_URL}</small>
                """,
                to: '2466065809@qq.com',
                attachmentsPattern: "${env.REPORT_FILENAME}"
            )
        }

        failure {
            echo "❌ 测试失败！但报告仍已生成: ${env.FULL_REPORT_PATH}"
            emailext (
                subject: "[FAILED] Pytest Report - Build #${BUILD_NUMBER}",
                body: """
                <h2>⚠️ 自动化测试失败！</h2>
                <p><strong>项目：</strong> pytest_jenkins</p>
                <p><strong>构建号：</strong> #${BUILD_NUMBER}</p>
                <p><strong>测试完成时间：</strong> ${env.REPORT_TIME}</p>
                <p>请查看附件中的 HTML 报告以排查失败用例。</p>
                <hr>
                <small>本邮件由 Jenkins 自动发送 | ${BUILD_URL}</small>
                """,
                to: '2466065809@qq.com',
                attachmentsPattern: "${env.REPORT_FILENAME}"
            )
        }
    }
}