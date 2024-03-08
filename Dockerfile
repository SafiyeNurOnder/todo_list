FROM python:3.10.12
MAINTAINER Safiye Nur Onder"safiyenuronder@gmail.com"
COPY app.py test.py /app/
WORKDIR /app
RUN pip install flask pytest flake8
CMD ["python", "app.py"]