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
