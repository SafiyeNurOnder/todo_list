FROM python:3.10-slim

LABEL maintainer="Safiye Nur Onder safiyenuronder@gmail.com"

WORKDIR /app

# Paket listelerini güncelle ve gerekli paketleri kur
RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    ffmpeg libsm6 libxext6 \
    libxcb-util1 \
    python3 \
    python3-pip \
    libssl-dev \
    pkg-config \
    qtbase5-dev \
    qtbase5-dev-tools \
    libqt5core5a \
    libqt5gui5 \
    libqt5widgets5 \
    libqt5svg5-dev \
    libqt5svg5
    #xvfb

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
ENV QT_QPA_PLATFORM_PLUGIN_PATH=/usr/lib/x86_64-linux-gnu/qt5/plugins/platforms
ENV XDG_RUNTIME_DIR=/tmp/runtime-root
#ENV LD_LIBRARY_PATH=/home/safiyenur/PycharmProjects/flask-hello-world-devops-project/.venv/lib/python3.10/site-packages/PyQt5/Qt5/lib/

# Gerekli dizini oluştur
RUN mkdir -p /tmp/runtime-root && chmod 0700 /tmp/runtime-root

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

# Uygulamayı çalıştır
CMD ["python3", "app.py"]
