pipeline {
    agent any

    environment {
        REPO_URL = 'https://github.com/SafiyeNurOnder/todo_list'
        APP_NAME = 'mytodolistapp'
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'master', url: "${REPO_URL}"
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    docker.image("${APP_NAME}:latest").inside {
                        sh 'Xvfb :99 &'
                        sh 'export DISPLAY=:99'
                        sh './venv/bin/python -m unittest discover -s tests'
                    }
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                def customImage = docker.build("${APP_NAME}:latest")
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

"""
pipeline {
    agent any

    stages {
        stage('Install Python3-venv') {
            steps {
                // `python3-venv` paketini yükle
                sh 'sudo apt-get update'
                sh 'sudo apt-get install -y python3-venv'
            }
        }

    stages {
        stage('Clone Repository') {
            steps {
                // Kod deposunu klonla
                git 'https://github.com/SafiyeNurOnder/todo_list'
            }
        }

        stage('Install Dependencies') {
            steps {
                // Python ortamını kur ve gereksinimleri yükle
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install -r requirements.txt'
                sh './venv/bin/pip install PyQt5 xmlrunner'
            }
        }

        stage('Run Tests') {
            steps {
                // Testleri çalıştır
                sh './venv/bin/python -m unittest discover -s tests'
            }
        }
    }

    post {
        always {
            // Test sonuçlarını raporla
            junit 'tests/reports/*.xml'
        }
    }
}
"""