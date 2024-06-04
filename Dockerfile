FROM python:3.10-slim

LABEL maintainer="Safiye Nur Onder safiyenuronder@gmail.com"

WORKDIR /app

# Paket listelerini güncelle ve gerekli paketleri kur
RUN apt-get update && apt-get install -y \
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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# PyQt5'in belirli bir sürümünü yükle
RUN pip3 install PyQt5==5.15.2
# Python bağımlılıklarını yükle
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY . .

# Ortam değişkenlerini ayarla
ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=1
ENV MYSQL_HOST=localhost
ENV MYSQL_DATABASE=todoList
ENV QT_QPA_PLATFORM_PLUGIN_PATH=/home/safiyenur/PycharmProjects/flask-hello-world-devops-project/.venv/lib/python3.10/site-packages/PyQt5/Qt/plugins/platforms
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
#ENV LD_LIBRARY_PATH=/home/safiyenur/PycharmProjects/flask-hello-world-devops-project/.venv/lib/python3.10/site-packages/PyQt5/Qt5/lib/

# Gerekli dizini oluştur
RUN mkdir -p /tmp/runtime-root && chmod 0700 /tmp/runtime-root

# Uygulamayı başlatmak için bir script oluştur
RUN echo '#!/bin/bash\n\
Xvfb :99 -screen 0 1024x768x24 &\n\
x11vnc -display :99 -nopw -forever -shared &\n\
python3 app.py' > /app/start.sh && chmod +x /app/start.sh

# Uygulamayı çalıştır
CMD ["/app/start.sh"]
