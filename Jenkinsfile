pipeline {
    agent any
    environment {
        IMAGE_NAME = "todo-app"
        CONTAINER_NAME = "todo-app-container"
        APP_PORT = "5000"
    }
    stages {
        stage('Code Build') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t $IMAGE_NAME .'
            }
        }
        stage('Unit Testing') {
            steps {
                echo 'Running unit tests...'
                sh '''
                    docker run --rm \
                        -v $WORKSPACE:/app \
                        -w /app \
                        $IMAGE_NAME \
                        pytest tests/test_unit.py -v --tb=short
                '''
            }
        }
        stage('Containerized Deployment') {
            steps {
                echo 'Deploying application...'
                sh '''
                    docker stop $CONTAINER_NAME || true
                    docker rm $CONTAINER_NAME || true
                    docker run -d \
                        --name $CONTAINER_NAME \
                        -p $APP_PORT:5000 \
                        $IMAGE_NAME
                    sleep 3
                    echo "App deployed at http://localhost:$APP_PORT"
                '''
            }
        }
        stage('Containerized Selenium Testing') {
            steps {
                echo 'Running Selenium tests in container...'
                sh '''
                    docker build -f Dockerfile.selenium -t selenium-tests .
                    docker run --rm \
                        --add-host=host.docker.internal:host-gateway \
                        selenium-tests
                '''
            }
        }
    }
    post {
        always {
            echo 'Pipeline finished.'
        }
        success {
            echo 'All stages passed!'
        }
        failure {
            echo 'Pipeline failed. Check logs above.'
            sh 'docker stop $CONTAINER_NAME || true'
        }
    }
}
