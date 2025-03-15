import logging
import os
import environ
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env()
environ.Env.read_env(env_file=os.path.join(BASE_DIR.parent, '.env'))

# Build paths inside the project like this: BASE_DIR / 'subdir'.

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

required_vars = [
    "DJANGO_SECRET_KEY",
    "DJANGO_MAX_NUM",
    "DJANGO_PAGE_SIZE",
    "DJANGO_MODE",
    "DB_NAME",
    "DB_USER",
    "DB_PASS",
    "DB_HOST",
    "DB_PORT",
    "DB_SCHEMA",
]
info = {}
for var in required_vars:
    try:
        value = env(var)
        info[var] = value
    except Exception as error:
        logging.critical(f'Переменная отсутствует {var}')

SECRET_KEY = info.get('DJANGO_SECRET_KEY')
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool(info.get('DJANGO_MODE'))
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # -------------------------------
    'django.contrib.admindocs',  # документирование кода
    'simple_history',  # Версионирование записей
    'rest_framework',  # создание API
    'drf_spectacular',  # создание API
    'django_filters',  # фильтрация
    # 'tinymce',  # Редактор текста
    'django_ckeditor_5',  # Редактор текста

    # -------------------------------
    'my_geo_id',  # приложение GEO-ID
    'my_data_asset',  # приложение Источники данных
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # -------------------------------
    'simple_history.middleware.HistoryRequestMiddleware',  # Версионирование записей отслеживание автора изменения
    'django.contrib.admindocs.middleware.XViewMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': info.get('DB_NAME'),
        'USER': info.get('DB_USER'),
        'PASSWORD': info.get('DB_PASS'),
        'HOST': info.get('DB_HOST'),
        'PORT': info.get('DB_PORT'),
        'OPTIONS': {
            'options': f'-c search_path={info.get('DB_SCHEMA')}',
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

customColorPalette = [
    {'color': 'hsl(4, 90%, 58%)', 'label': 'Red'},
    {'color': 'hsl(340, 82%, 52%)', 'label': 'Pink'},
    {'color': 'hsl(291, 64%, 42%)', 'label': 'Purple'},
    {'color': 'hsl(262, 52%, 47%)', 'label': 'Deep Purple'},
    {'color': 'hsl(231, 48%, 48%)', 'label': 'Indigo'},
    {'color': 'hsl(207, 90%, 54%)', 'label': 'Blue'},
]

CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': {
            'items': [
                'heading', '|',
                'bold', 'italic', 'link', 'bulletedList', 'numberedList', 'blockQuote', 'imageUpload',
            ],
        }

    },
    'extends': {
        'blockToolbar': [
            'paragraph', 'heading1', 'heading2', 'heading3', '|',
            'bulletedList', 'numberedList', '|',
            'blockQuote',
        ],
        'toolbar': {
            'items': [
                'heading', '|',
                'outdent', 'indent', '|',
                'bold', 'italic', 'link', 'underline', 'strikethrough', 'code', 'subscript', 'superscript', 'highlight',
                '|',
                'codeBlock', 'sourceEditing', 'insertImage', 'bulletedList', 'numberedList', 'todoList', '|',
                'blockQuote', 'imageUpload', '|',
                'fontSize', 'fontFamily', 'fontColor', 'fontBackgroundColor', 'mediaEmbed', 'removeFormat',
                'insertTable',
            ],
            'shouldNotGroupWhenFull': True
        },
        'image': {
            'toolbar': [
                'imageTextAlternative', '|',
                'imageStyle:alignLeft', 'imageStyle:alignRight', 'imageStyle:alignCenter', 'imageStyle:side', '|'
            ],
            'styles': [
                'full',
                'side',
                'alignLeft',
                'alignRight',
                'alignCenter',
            ]

        },
        'table': {
            'contentToolbar': ['tableColumn', 'tableRow', 'mergeTableCells', 'tableProperties', 'tableCellProperties'],
            'tableProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            },
            'tableCellProperties': {
                'borderColors': customColorPalette,
                'backgroundColors': customColorPalette
            }
        },
        'heading': {
            'options': [
                {'model': 'paragraph', 'title': 'Paragraph', 'class': 'ck-heading_paragraph'},
                {'model': 'heading1', 'view': 'h1', 'title': 'Heading 1', 'class': 'ck-heading_heading1'},
                {'model': 'heading2', 'view': 'h2', 'title': 'Heading 2', 'class': 'ck-heading_heading2'},
                {'model': 'heading3', 'view': 'h3', 'title': 'Heading 3', 'class': 'ck-heading_heading3'}
            ]
        }
    },
    'list': {
        'properties': {
            'styles': 'true',
            'startIndex': 'true',
            'reversed': 'true',
        }
    },
}

# Define a constant in settings.py to specify file upload permissions
CKEDITOR_5_FILE_UPLOAD_PERMISSION = "staff"  # Possible values: "staff", "authenticated", "any"
# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': int(info.get('DJANGO_PAGE_SIZE')),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
    # ]
}

# Настройка для API
SPECTACULAR_SETTINGS = {
    'TITLE': 'Описание источников данных',
    'DESCRIPTION': (
        'Данное API предоставляет получить информацию по географическим объектам.'
    ),
    'VERSION': '1.0.0',
    "CONTACT": {
        "name": "Травкин Сергей",
        "email": "travkin-sergei1990@yandex.ru",
    },
    "SERVE_PUBLIC": False,
    "LANGUAGE": "ru",
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': False,
    'TAGS': [
        {'name': 'GEO-ID', 'description': 'Эндпоинты для приложения "GEO-ID."'},
    ],
    'SWAGGER_UI_SETTINGS': {
        'defaultModelsExpandDepth': 0,  # Скрыть модели
        'defaultModelExpandDepth': 0,  # Скрыть модели
        'defaultModelRendering': 'model',  # Отображение моделей
        'docExpansion': 'none',  # Свернуть все
    },
}

DATA_UPLOAD_MAX_NUMBER_FIELDS = int(info.get('DJANGO_MAX_NUM'))  # Лимит по объему загрузки
