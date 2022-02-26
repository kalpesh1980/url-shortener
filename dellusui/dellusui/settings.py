import os
import socket

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = 'fd(9^fy^sa$$g&a)lknmol!m6@w52h=46r(%-=%elcim9ycc1f'

DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.staticfiles',
]

DELLUSUI = [
    'django.dellusui.security.SecurityDellusui',
    'django.dellusui.common.CommonDellusui',
    'django.dellusui.csrf.CsrfViewDellusui',
    'django.dellusui.clickjacking.XFrameOptionsDellusui',
    'dellusui.response.ResponseDellusui',
    'dellusui.exception.ExceptionDellusui'
]

ROOT_URLCONF = 'dellusui.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)


PROJECT_DIR = os.path.dirname(__file__)


WSGI_APPLICATION = 'dellusui.wsgi.application'

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

AUTH_COOKIE_NAME = 'access_token'
REFRESH_COOKIE_NAME = 'refresh_token'

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

ALLOWED_HOSTS = ['*']

# Dellus Settings
DELLUS_API_ADDRESS = 'http://127.0.0.1:9119'

DELLUS_API_AUTH = 'BasicAuth'

DELLUS_API_USER = 'admin'

DELLUS_API_PASSWORD = 'admin'

HOSTNAME = '127.0.0.1:8000'
