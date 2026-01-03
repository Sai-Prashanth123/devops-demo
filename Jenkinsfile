pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Sai-Prashanth123/devops-demo.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t fastapi-app .'
            }
        }

        stage('Run Container') {
            steps {
                sh '''
                docker stop fastapi || true
                docker rm fastapi || true
                docker run -d -p 8000:8000 --name fastapi fastapi-app
                '''
            }
        }
    }
}
