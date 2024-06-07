pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'safiyenuronder/mytodolistapp:latest'  // Docker Hub'daki imajınızın ismi ve etiketi
        DISPLAY = ':99'  // Xvfb için kullanılacak ekran numarası
        DOCKER_VOLUME = 'mytodolistapp_data'
    }

    stages {
        stage('Pull Docker Image') {
            steps {
                script {
                    sh "docker pull ${DOCKER_IMAGE}"
                }
            }
        }

        stage('Setup Xvfb') {
            steps {
                sh 'Xvfb :99 -screen 0 1024x768x24 &'
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh "docker run -e DISPLAY=${DISPLAY} -v ${DOCKER_VOLUME}:/app -w /app ${DOCKER_IMAGE} python -m unittest discover -s tests"
                }
            }
        }
    }

    post {
        always {
            junit 'tests/reports/*.xml'
        }
    }
}