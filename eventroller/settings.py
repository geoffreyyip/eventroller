"""
Django settings for eventroller project.

Generated by 'django-admin startproject' using Django 1.8.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'l^7aj1l)+r(@9haz!_(w#8gp=u3ikl_0w$4cb89^-sb!&ur6p!'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ('DEBUG' in os.environ)

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'event_store',
    'reviewer',
    'event_exim',
    'event_review',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'eventroller.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'eventroller.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

if 'DB_HOSTNAME' in os.environ:
    DATABASES['default'] = {
            'ENGINE': os.environ.get('DB_ENGINE', 'django.db.backends.postgresql_psycopg2'),
            'NAME': os.environ['DB_NAME'],
            'USER': os.environ['DB_USERNAME'],
            'PASSWORD': os.environ['DB_PASSWORD'],
            'HOST': os.environ['DB_HOSTNAME'],
            'PORT': os.environ['DB_PORT'],
    }

#enable in cachalot local_settings when setting CACHES=
#short table, and campaigns should update more often than other queries
CACHALOT_UNCACHABLE_TABLES = ('events_campaign', 'events_event',)
CACHALOT_ENABLED = False
if 'REDISCACHE' in os.environ:
    CACHES = {
        'default': {
            "BACKEND": "django_redis.cache.RedisCache",
            "LOCATION": os.environ['REDISCACHE'].split(','), #"redis://127.0.0.1:6379/1",
            "OPTIONS": {
                "CLIENT_CLASS": "django_redis.client.DefaultClient",
            },
            'KEY_PREFIX': os.environ.get('CACHE_PREFIX', ''),
        },
    }
    if settings.DEBUG:
        CACHES['default']['OPTIONS']["REDIS_CLIENT_CLASS"] = "fakeredis.FakeStrictRedis"

    CACHALOT_ENABLED = True

EVENT_SOURCES = json.loads(os.environ.get('EVENT_SOURCES', '{}'))

BASE_URL = os.environ.get('BASE_URL')

EMAIL_HOST = os.environ.get('EMAIL_HOST', '')
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER', '')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD', '')
EMAIL_PORT = os.environ.get('EMAIL_PORT', '')
EMAIL_USE_TLS = True

FORCE_SCRIPT_NAME = None

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = os.environ.get('STATIC_URL', '/static/')
STATIC_ROOT = '%s/static_build' % BASE_DIR

if os.environ.get('LAMBDA_ZAPPA'):
    SECRET_KEY = os.environ.get('DJANGO_BASE_SECRET', SECRET_KEY)
    if os.environ.get('ALLOWED_HOSTS'):
        ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS').split(',')
    if 'FORCE_SCRIPT_NAME' in os.environ:
        #this is for the prefix in deployed state before the / in the path
        FORCE_SCRIPT_NAME = os.environ['FORCE_SCRIPT_NAME']

if not os.environ.get('LAMBDA_ZAPPA') \
   and os.path.exists(os.path.join(BASE_DIR, 'local_settings.py')):
    from local_settings import *
