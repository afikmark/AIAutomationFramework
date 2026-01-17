pipeline {
    agent any

    options {
        timeout(time: 30, unit: 'MINUTES')
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
        timestamps()
    }

    environment {
        DOCKER_BUILDKIT = '1'
        BASE_IMAGE = 'ai-automation-framework-base'
        TEST_IMAGE = 'ai-automation-framework-test'
        ALLURE_RESULTS = 'allure-results'
    }

    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Git branch to checkout and run tests from')
        string(name: 'PYTEST_ARGS', defaultValue: 'tests', description: 'Pytest arguments (e.g., "tests -m sanity" or "tests/sauce_ui")')
        string(name: 'PARALLEL_WORKERS', defaultValue: 'auto', description: 'Number of parallel workers for pytest-xdist')
        booleanParam(name: 'REBUILD_BASE_IMAGE', defaultValue: false, description: 'Force rebuild of the base Docker image')
    }

    stages {
        stage('Checkout') {
            steps {
                script {
                    checkout([
                        $class: 'GitSCM',
                        branches: [[name: "*/${params.BRANCH}"]],
                        userRemoteConfigs: scm.userRemoteConfigs
                    ])
                }
            }
        }

        stage('Build Base Image') {
            steps {
                script {
                    def baseImageExists = sh(
                        script: "docker images -q ${BASE_IMAGE}:latest 2>/dev/null",
                        returnStatus: true
                    ) == 0
                    
                    if (params.REBUILD_BASE_IMAGE || !baseImageExists) {
                        echo "Building base image..."
                        docker.build("${BASE_IMAGE}:latest", "-f ci/base.Dockerfile .")
                    } else {
                        echo "Base image exists, skipping build. Use REBUILD_BASE_IMAGE=true to force rebuild."
                    }
                }
            }
        }

        stage('Build Test Image') {
            steps {
                script {
                    // Ensure base image exists
                    def baseImageExists = sh(
                        script: "docker images -q ${BASE_IMAGE}:latest 2>/dev/null",
                        returnStatus: true
                    ) == 0
                    
                    if (!baseImageExists) {
                        echo "Base image not found, building it first..."
                        docker.build("${BASE_IMAGE}:latest", "-f ci/base.Dockerfile .")
                    }
                    
                    echo "Building test image..."
                    docker.build("${TEST_IMAGE}:${BUILD_NUMBER}", "-f ci/test.Dockerfile .")
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Create allure-results directory with proper permissions
                    sh "mkdir -p ${ALLURE_RESULTS} && chmod 777 ${ALLURE_RESULTS}"

                    def pytestArgs = [
                        '--alluredir=/app/allure-results',
                        params.PYTEST_ARGS
                    ]

                    if (params.PARALLEL_WORKERS != '1') {
                        pytestArgs.add("-n ${params.PARALLEL_WORKERS}")
                    }

                    def pytestCommand = "uv run pytest ${pytestArgs.join(' ')}"

                    // Run container with Jenkins user ID to avoid permission issues
                    sh """
                        docker run --rm \
                            --user \$(id -u):\$(id -g) \
                            -v \${WORKSPACE}/${ALLURE_RESULTS}:/app/allure-results \
                            -e HOME=/tmp \
                            -e PLAYWRIGHT_BROWSERS_PATH=/ms-playwright \
                            ${TEST_IMAGE}:${BUILD_NUMBER} \
                            ${pytestCommand}
                    """

                    // Fix permissions on allure-results after test run
                    sh "chmod -R 755 ${ALLURE_RESULTS} || true"
                }
            }
        }
    }

    post {
        always {
            // Archive test artifacts first (before any cleanup)
            archiveArtifacts artifacts: "/**/*", allowEmptyArchive: true

            script {
                // Generate Allure report if plugin is configured
                try {
                    allure([
                        includeProperties: false,
                        jdk: '',
                        commandline: 'allure-tool',
                        results: [[path: "${ALLURE_RESULTS}"]]
                    ])
                } catch (Exception e) {
                    echo "Allure report generation skipped: ${e.message}"
                    echo "To enable Allure reports, configure Allure Commandline in Jenkins Global Tool Configuration"
                }
            }

            // Clean up Docker images
            sh """
                docker rmi ${TEST_IMAGE}:${BUILD_NUMBER} || true
            """
        }

        success {
            echo 'Tests passed successfully!'
        }

        failure {
            echo 'Tests failed. Check the Allure report for details.'
        }

        cleanup {
            cleanWs()
        }
    }
}