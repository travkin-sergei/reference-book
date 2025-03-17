
FROM python:3.12

LABEL maintainer="stravkin"

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY mysite mysite
COPY .env .env

# Укажите команду для запуска вашего приложения
CMD ["python", "mysite/manage.py", "runserver", "0.0.0.0:8000"]