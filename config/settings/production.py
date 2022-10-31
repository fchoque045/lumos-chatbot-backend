from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['chatbot.promace.jujuy.edu.ar', 'chatbot.promace2.jujuy.edu.ar', 'promace.jujuy.edu.ar',
                 'promace2.jujuy.edu.ar', 'promace3.jujuy.edu.ar', 'localhost']

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

CSRF_TRUSTED_ORIGINS = [
    'https://chatbot.promace.jujuy.edu.ar', 'https://chatbot.promace2.jujuy.edu.ar', 'https://promace.jujuy.edu.ar', 'https://promace2.jujuy.edu.ar', 'https://promace3.jujuy.edu.ar', 'http://localhost']
CSRF_COOKIE_SECURE = False
