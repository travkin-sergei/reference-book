# Справочники

## Список приложений:

1. my_data_asset - это справочник источников данных
2. my_geo_id - это справочник гео объектов


## Технологии

1. Django- основной фреймворк
2. django-filter - фильтрация данных (выборка из базы)
3. djangorestframework
4. drf-spectacular - документирвоание API
5. django-ckeditor - редактор текста
6. PostgreSQL - база данных

## Запуск:

1. Создать виртуальное окружение
2. запустить команду pip install -r requirements.txt
3. сгенерировать свой SECRET_KEY

```commandline
python3 -c "import secrets; print(secrets.token_urlsafe())"
```
4. в корневой директории создать файл ".env"

# Как собрать образ?
Все написано для запуска на локальной машине!
## Наличие Docker обязательно
## Сборка образа
```bash
  docker build -t your_image_name .
```
## Запуск контейнера
```bash
  docker run -p 8000:8000 your_image_name
```
## Открыть ссылку на приложение
[Перейти на локальный сервер http://127.0.0.1:8000](http://127.0.0.1:8000/)
```commandline
DJANGO_SECRET_KEY=django-insecure-*********************************
DJANGO_MAX_NUM=10000
DJANGO_PAGE_SIZE=1000
DJANGO_MODE=1

DB_NAME=reference_book
DB_USER=postgres
DB_PASS=123456
DB_HOST=localhost
DB_PORT=5432
DB_SCHEMA=******
```

## Структура проекта

### Обязательные шаблоны (templates):

1. about_application.html - Описание приложения!
2. _nav.html - меню приложения:
```html
app_name - имя приложения.
<li class="nav-item dropdown">
    <a class="nav-link dropdown-toggle" href="#" role="button" id="navbarDropdown" data-bs-toggle="dropdown"
       aria-expanded="false">
        Геообъекты
    </a>
    <ul class="dropdown-menu" aria-labelledby="navbarDropdown">
        <li>
            <a class="dropdown-item" href="{% url 'app_name:about-app' %}">
                О разделе
            </a>
        </li>
    </ul>
</li>
```

templates/_inc/_nav.html в этот шаблон добавить 

```html
<ul class="navbar-nav me-auto mb-2 mb-lg-0">
    {% include 'app_name1/_nav.html' %}
    {% include 'app_name2/_nav.html' %}
    ...
</ul>
```

# Дополнительные комментарии
База данных должна быть локально на машине, а не в контейнере. делал под себя!!!  

Обращаю внимание на допущения которые я сделал.
файл .env
```shell
DJANGO_SECRET_KEY=django-insecure-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
DJANGO_MAX_NUM=10000
DJANGO_PAGE_SIZE=1000
DJANGO_MODE=1

DB_DEFAULT_NAME=XXXXXXXXXXXXXXXX
DB_DEFAULT_USER=postgres
DB_DEFAULT_PASS=123456
DB_DEFAULT_HOST=host.docker.internal
DB_DEFAULT_PORT=5432
DB_SCHEMA=my_default,my_geo_id,my_data_asset
```

.dockerignore
```
    # .env/
```
Dockerfile
```shell
  COPY .env .env
```