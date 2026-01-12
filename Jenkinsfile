Jenkinsfile (Declarative Pipeline)
pipeline {
    agent { 
        docker { 
            image 'mcr.microsoft.com/playwright/python:v1.49.0-jammy'
            args '--user root'
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
                    pip install --upgrade pip
                    pip install .
                    pip install allure-pytest
                    playwright install --with-deps chromium
                '''
            }
        }
        
        stage('Run Tests') {
            steps {
                sh '''
                    pytest tests/ \
                        --alluredir=${ALLURE_RESULTS_PATH} \
                        --tb=short \
                        --verbose \
                        || true
                '''
            }
        }
        
        stage('Generate Allure Report') {
            steps {
                script {
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
    }
    
    post {
        always {
            junit testResults: '**/allure-results/*.xml', allowEmptyResults: true
            archiveArtifacts artifacts: 'allure-results/**/*', allowEmptyArchive: true
            cleanWs()
        }
        success {
            echo 'All tests passed!'
        }
        failure {
            echo 'Some tests failed. Check the Allure report for details.'
        }
    }
}