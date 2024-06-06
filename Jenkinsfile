pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/SafiyeNurOnder/todo_list.git'
            }
        }

        stage('Install xvfb') {
            steps {
                sh 'sudo apt-get update && sudo apt-get install -y xvfb'
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh 'python -m venv venv'
                sh './venv/bin/pip install --upgrade pip'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh './venv/bin/pip install -r requirements.txt'
                sh './venv/bin/pip install unittest-xml-reporting'
            }
        }

        stage('Run Tests') {
            steps {
                sh './venv/bin/python -m xmlrunner discover -s tests -p "*.py" -o test-reports'
            }
        }
    }

    post {
        always {
            junit 'test-reports/*.xml'
        }
    }
}

"""pipeline {
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
}"""
