# Справочники"

## Технологии

1. Django==5.0.7 - основной фреймворк
2. django-filter - фильтрация данных (выборка из базы)
3. djangorestframework==3.15.2 
4. drf-spectacular - документирвоание API 
5. django-ckeditor - редактор текста

## Запуск:
1. Создать виртуальное окружение
2. запустить команду pip install -r requirements.txt
3. сгенерировать свой SECRET_KEY
```commandline
python3 -c "import secrets; print(secrets.token_urlsafe())"
```
4. в корневой директории создать файл ".env"
```commandline
SECRET_KEY=django-insecure-*************************************************
DB_NAME=reference_book
DB_USER=postgres
DB_PASS=123456
DB_HOST=localhost
DB_PORT=5432
DB_SCHEMA=reference_book
```


## Список приложений:

1. geo_object - это справочник гео объектов