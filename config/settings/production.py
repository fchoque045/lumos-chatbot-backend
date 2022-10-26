from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['https://chatbot.promace.jujuy.edu.ar', 'https://promace.jujuy.edu.ar',
                 'https://promace2.jujuy.edu.ar', 'https://promace3.jujuy.edu.ar']

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    }
}

CORS_ALLOW_ALL_ORIGINS = True

CORS_ALLOW_HEADERS = [
    "Access-Control-Allow-Origin",
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

CSRF_COOKIE_SECURE = False
ALLOWED_HOST = ['https://chatbot.promace.jujuy.edu.ar', 'https://promace.jujuy.edu.ar',
                'https://promace2.jujuy.edu.ar', 'https://promace3.jujuy.edu.ar']
CSRF_TRUSTED_ORIGINS = ['https://chatbot.promace.jujuy.edu.ar', 'https://promace.jujuy.edu.ar',
                        'https://promace2.jujuy.edu.ar', 'https://promace3.jujuy.edu.ar']
