pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/SafiyeNurOnder/todo_list.git'
            }
        }

        stage('Install System Dependencies') {
            steps {
                sh '''
                sudo apt-get update && sudo apt-get install -y \
                    build-essential \
                    ffmpeg libsm6 libxext6 \
                    libxcb1 \
                    libx11-xcb1 \
                    libxcb-glx0 \
                    libxcb-keysyms1 \
                    libxcb-image0 \
                    libxcb-shm0 \
                    libxcb-icccm4 \
                    libxcb-render0 \
                    libxcb-xkb1 \
                    libxcb-randr0 \
                    libxcb-xinerama0 \
                    libxcb-util1 \
                    libxkbcommon-x11-0 \
                    libxkbcommon0 \
                    libssl-dev \
                    pkg-config \
                    wget \
                    default-libmysqlclient-dev \
                    python3 \
                    python3-pip \
                    qtbase5-dev \
                    qtbase5-dev-tools \
                    libqt5core5a \
                    libqt5gui5 \
                    libqt5widgets5 \
                    libqt5svg5-dev \
                    libqt5svg5 \
                    libgl1-mesa-glx \
                    libglib2.0-0 \
                    libpulse0 \
                    dbus \
                    libfontconfig1 \
                    libdbus-1-3 \
                    libharfbuzz0b \
                    libxrender1 \
                    libxcursor1 \
                    libxi6 \
                    libxtst6 \
                    libxcomposite1 \
                    libxdamage1 \
                    libxrandr2 \
                    libcap2 \
                    libatk1.0-0 \
                    libatk-bridge2.0-0 \
                    libxss1 \
                    libnss3 \
                    libasound2 \
                    xvfb \
                    && sudo apt-get clean \
                    && sudo rm -rf /var/lib/apt/lists/*
                '''
            }
        }

        stage('Setup Python Environment') {
            steps {
                sh 'python3 -m venv venv'
                sh './venv/bin/pip install --upgrade pip'
            }
        }

        stage('Install Python Dependencies') {
            steps {
                sh './venv/bin/pip install -r requirements.txt'
                sh './venv/bin/pip install PyQt5==5.15.2'
                sh './venv/bin/pip install unittest-xml-reporting'
            }
        }

        stage('Run Tests') {
            steps {
                RUN echo '#!/bin/bash\n\
                Xvfb :99 -screen 0 1024x768x24 &\n\
                x11vnc -display :99 -nopw -forever -shared &\n\
                    python3 app.py' > /app/start.sh && chmod +x /app/start.sh


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
                sh 'xvfb-run -a ./venv/bin/python -m xmlrunner discover -s tests -p "*.py" -o test-reports'
            }
        }
    }

    post {
        always {
            junit 'test-reports/*.xml'
        }
    }
}"""

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
