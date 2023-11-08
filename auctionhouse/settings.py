"""
Django settings for auctionhouse project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
from dotenv import load_dotenv
import django
from django.utils.encoding import smart_str

load_dotenv()

# fix for smart text and django v4
django.utils.encoding.smart_text = smart_str

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SUPER_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

allowed_hosts_string = os.getenv('ALLOWED_HOSTS')
allowed_hosts_array = allowed_hosts_string.split(",")
ALLOWED_HOSTS = ["poptape.club"]
# ALLOWED_HOSTS = allowed_hosts_array
ENVIRONMENT = os.getenv('ENVIRONMENT')


# Application definition

INSTALLED_APPS = [
    'django.contrib.postgres',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_extensions',
    'background_task',
    # 'django_nose',
    'djmoney',
    'auction',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
        'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.SessionAuthentication',
        # 'auctionhouse.authentication.AdminOnlyAuthentication',
        'auctionhouse.authentication.TokenAuth',
        'auctionhouse.authentication.CsrfExemptSessionAuthentication',
        'auctionhouse.authentication.AdminOnlyAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.BasicAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ],
    'TEST_REQUEST_DEFAULT_FORMAT': 'json',
    # we only want to accept json input so default to json only
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
    )
}

# logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(levelname)-8s] [%(asctime)s] [%(process)d] [%(thread)d] %(module)s - %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.getenv('LOGFILE'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': False,
        },
        'auctionhouse': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'auction': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}

# url stuff
ROOT_URLCONF = 'auctionhouse.urls'
APISERVER_URL = 'apiserver/'
AUTH_URL = 'authy/'
ADDRESS_URL = 'address/'

# NOTE: if running in docker use set these to internal docker network names
# to avoid trips out to the internet when calling the microservice
APISERVER_SERVER = os.getenv('APISERVER_URL')
AUTH_SERVER_URL = os.getenv('AUTH_SERVER_URL')
AUTH_SERVER_ADMIN_URL = os.getenv('AUTH_SERVER_ADMIN_URL')
FOTOS_SERVER_URL = os.getenv('FOTOS_SERVER_URL')
ADDRESS_SERVER_URL = os.getenv('ADDRESS_SERVER_URL')

RABBIT_IP = os.getenv('RABBIT_IP')
RABBIT_USER = os.getenv('RABBIT_USER')
RABBIT_PASS = os.getenv('RABBIT_PASS') 
RABBIT_VHOST = os.getenv('RABBIT_VHOST') 
RABBIT_PORT = os.getenv('RABBIT_PORT')

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

WSGI_APPLICATION = 'auctionhouse.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('AUCTIONHOUSE_DB_NAME'),
        'USER': os.getenv('AUCTIONHOUSE_DB_USER'),
        'PASSWORD': os.getenv('AUCTIONHOUSE_DB_PASS'),
        'HOST': os.getenv('AUCTIONHOUSE_DB_HOST'),
        'PORT': os.getenv('AUCTIONHOUSE_DB_PORT'),
        'TEST': {
            'NAME': os.getenv('TEST_AUCTIONHOUSE_DB_NAME'),
            'USER': os.getenv('TEST_AUCTIONHOUSE_DB_USER'),
            'PASSWORD': os.getenv('TEST_AUCTIONHOUSE_DB_PASS'),
            'HOST': os.getenv('TEST_AUCTIONHOUSE_DB_HOST'),
            'PORT': os.getenv('TEST_AUCTIONHOUSE_DB_PORT'),
        }
        # 'ATOMIC_REQUESTS': True,
    }
}

# get rid of DEFAULT_AUTO_FIELD warnings
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Use nose to run all tests
# TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

# Tell nose to measure coverage on the 'foo' and 'bar' apps
# NOSE_ARGS = [
#    '--with-coverage',
#    '--cover-package=auctionhouse,auction',
# ]


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
STATIC_URL = '/auctionhouse/static/'
