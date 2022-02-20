from datetime import timedelta
from .base import *


SECRET_KEY = '5f5bb7a0-16b8-4dae-8583-afdf5c4f92f1'

ALLOWED_HOSTS = ['*']

DEBUG = False

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=10),
    'AUTH_TOKEN_CLASSES':('api.auth.simplejwt.token.AccessToken',)
}