"""
Django settings for the demo project.

Please refer to the documentation for more information.
"""

import os
from pathlib import Path
from os.path import dirname, abspath, join, normpath

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
# demo_project/
DEMO_ROOT = Path(os.path.dirname(__file__)) / '..'
# tests/
TEST_ROOT = DEMO_ROOT / '..'
# django-cruds-adminlte folder (the one with setup.py)
ROOT = TEST_ROOT / '..'

SECRET_KEY = 's*pq#9=$v7+acw$1gj0-x1b)#-$oxa)zr)r%@(@xu7g%u17(ll'
DEBUG = True
ALLOWED_HOSTS = []
INTERNAL_IPS = ('127.0.0.1',)
PASSWORD_HASHERS = ["django.contrib.auth.hashers.MD5PasswordHasher"]

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'crispy_forms',
    'django_select2',
    'easy_thumbnails',
    'image_cropping',
    'cruds_adminlte',
    'django_ajax',
    'testapp',
    'demo',
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

ROOT_URLCONF = 'demo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            str(DEMO_ROOT / 'demo' / 'templates'),
        ],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                'cruds_adminlte.template_loader.Loader',
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        }
    },
]

WSGI_APPLICATION = 'demo.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': str(DEMO_ROOT / 'db.sqlite3'),
    }
}

AUTH_PASSWORD_VALIDATORS = [ ]

LOGIN_REDIRECT_URL = '/login'

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

TIME_FORMAT = 'h:i A'
DATETIME_FORMAT = 'm/d/Y H:i:s'
DATE_FORMAT = "m/d/Y"
TIME_INPUT_FORMATS = ['%I:%M %p']

STATIC_URL = '/static/'
CRISPY_TEMPLATE_PACK = 'bootstrap3'
STATIC_ROOT = str(DEMO_ROOT / 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = str(DEMO_ROOT / 'media') 

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

TEST_USER_EMAIL = 'fulano.mengano@example.com'
TEST_USER_PASSWORD = 'godofredo'

# easy_thumbnails
from easy_thumbnails.conf import Settings as thumbnail_settings
THUMBNAIL_PROCESSORS = (
    'image_cropping.thumbnail_processors.crop_corners',
) + thumbnail_settings.THUMBNAIL_PROCESSORS
IMAGE_CROPPING_JQUERY_URL = None
