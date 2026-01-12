pipeline {
    agent { 
        docker { 
            image 'mcr.microsoft.com/playwright/python:v1.49.0-noble'
        } 
    }
    
    environment {
        ALLURE_RESULTS_PATH = 'allure-results'
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''
                    python --version
                    pip install --upgrade pip uv
                    export PATH="$HOME/.local/bin:$PATH"
                    uv pip install --system .
                    uv pip install --system allure-pytest
                    playwright install --with-deps chromium
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    def testResult = sh(
                        script: '''
                            export PYTHONPATH="${WORKSPACE}:${PYTHONPATH}"
                            pytest tests/ \
                                --alluredir=${ALLURE_RESULTS_PATH} \
                                --junitxml=test-results.xml \
                                --tb=short \
                                --verbose
                        ''',
                        returnStatus: true
                    )
                    env.TEST_EXIT_CODE = testResult.toString()
                }
            }
        }
        
        stage('Generate Allure Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    properties: [],
                    reportBuildPolicy: 'ALWAYS',
                    results: [[path: "${env.ALLURE_RESULTS_PATH}"]]
                ])
            }
        }
    }
    
    post {
        always {
            junit testResults: 'test-results.xml', allowEmptyResults: true
            archiveArtifacts artifacts: 'allure-results/**/*,test-results.xml', allowEmptyArchive: true
            cleanWs()
        }
        success {
            script {
                if (env.TEST_EXIT_CODE == '0') {
                    echo 'All tests passed!'
                } else {
                    echo "Build successful but some tests may have issues. Exit code: ${env.TEST_EXIT_CODE}"
                }
            }
        }
        failure {
            echo 'Pipeline failed. Check the logs for details.'
        }
        unstable {
            echo 'Some tests failed. Check the test results for details.'
        }
    }
}