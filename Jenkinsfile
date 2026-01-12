pipeline {
    agent {
        docker {
            // Using a Playwright-ready image to save time on system dependencies
            image 'mcr.microsoft.com/playwright/python:v1.49.0-noble'
            args  '--user root' // Ensure permissions to create directories
        }
    }

    environment {
        // Force Python to output logs immediately to Jenkins console
        PYTHONUNBUFFERED = '1'
        PYTHONDONTWRITEBYTECODE = '1'
    }

    stages {
        stage('Initialize') {
            steps {
                sh 'python3 --version'
                // Install the project and dependencies directly into the container
                sh 'pip install --upgrade pip'
                sh 'pip install -e .[dev]'
            }
        }

        stage('Static Analysis') {
            parallel {
                stage('Linting') {
                    steps {
                        sh 'black --check .'
                    }
                }
                stage('Type Checking') {
                    steps {
                        sh 'mypy .'
                    }
                }
            }
        }

        stage('Execute Automation') {
            steps {
                script {
                    // Running with xdist for speed and allure for reporting
                    sh 'pytest -n auto --alluredir=allure-results'
                }
            }
        }
    }

    post {
        always {
            // Archive the Allure results for the Jenkins plugin
            allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            
            // Archive local screenshots/logs as artifacts for quick debugging
            archiveArtifacts artifacts: 'allure-results/*.png', allowEmptyArchive: true
        }
        cleanup {
            // Remove build artifacts to keep the workspace light
            cleanWs()
        }
    }
}