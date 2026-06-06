pipeline {
    agent any

    environment {
        // Defines the name tag for your local Docker image
        IMAGE_NAME = "python-jenkins-demo:${BUILD_NUMBER}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test Inside Docker') {
            agent {
                // Runs this specific stage inside an ephemeral Python container
                docker { 
                    image 'python:3.11-slim'
                    // Reuses the workspace to store test artifacts
                    args '-v /tmp:/tmp' 
                }
            }
            steps {
                sh '''
                    pip install -r requirements.txt
                    pytest test_app.py --junitxml=results.xml
                '''
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building production Docker image..."
                // Builds the Dockerfile in the root directory
                sh "docker build -t ${IMAGE_NAME} ."
            }
        }

        stage('Run Docker Container') {
            steps {
                echo "Testing container runtime..."
                // Runs the newly built container to verify output
                sh "docker run --rm ${IMAGE_NAME}"
            }
        }
    }

    post {
        always {
            // Publishes the test results graph on the Jenkins dashboard
            junit 'results.xml'
        }
        success {
            echo "Pipeline complete! Image ${IMAGE_NAME} is ready for deployment."
        }
        cleanup {
            // Cleans up old images from the Jenkins agent host to save space
            sh "docker rmi ${IMAGE_NAME} || true"
        }
    }
}
