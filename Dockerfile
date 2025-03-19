# Используем Python 3.12
FROM python:3.12

LABEL maintainer="stravkin"

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Копируем код приложения
COPY mysite mysite
COPY .env .env

# Открываем порт для Django
EXPOSE 8000

# Запуск Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "mysite.wsgi:application", "--chdir", "/app/mysite"]

