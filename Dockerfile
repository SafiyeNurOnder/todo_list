FROM python:3.9

LABEL maintainer="Safiye Nur Onder safiyenuronder@gmail.com"

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    ffmpeg libsm6 libxext6

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV MYSQL_USER=root
ENV MYSQL_PASSWORD=1
ENV MYSQL_HOST=192.168.49.1
ENV MYSQL_DATABASE=todoList

CMD ["python", "app.py"]
