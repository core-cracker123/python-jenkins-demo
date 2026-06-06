pipeline {
    agent any

    environment {
        IMAGE_NAME = "python-jenkins-demo:${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test Inside Docker') {
            steps {
                echo "Running tests inside an ephemeral Docker container..."
                // Using a script block to safely handle test failures without breaking the build
                script {
                    try {
                        sh '''
                            docker run --rm -v "$(pwd)":/app -w /app python:3.11-slim sh -c "
                                pip install --no-cache-dir -r requirements.txt &&
                                pytest test_app.py --junitxml=results.xml
                            "
                        '''
                    } catch (Exception e) {
                        // Mark build as unstable if tests fail, but do not stop the pipeline completely
                        currentBuild.result = 'UNSTABLE'
                        echo "Testing completed with failures: ${e.message}"
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building production Docker image..."
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Run Docker Container') {
            steps {
                echo "Testing container runtime..."
                sh "docker run --rm ${IMAGE_NAME}"
            }
        }
    }

    post {
        always {
            // Jenkins will parse this XML even if tests fail
            junit allowEmptyResults: true, testResults: 'results.xml'
        }
        cleanup {
            sh "docker rmi ${IMAGE_NAME} || true"
        }
    }
}
