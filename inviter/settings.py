import os
import string
from main.mailer import Mailer

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = os.environ.get('INVITER_SECRET_KEY', 'invalid_secret_key')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
ALLOWED_HOSTS = ['inviter.ru']

INSTALLED_APPS = [
    'main',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'inviter.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth'
            ],
        },
    },
]

WSGI_APPLICATION = 'inviter.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'inviter.sqlite3'),
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

PWMP = 'django.contrib.auth.password_validation.'
AUTH_PASSWORD_VALIDATORS = [{
    'NAME': PWMP + 'UserAttributeSimilarityValidator'}, {
    'NAME': PWMP + 'MinimumLengthValidator'}, {
    'NAME': PWMP + 'CommonPasswordValidator'}, {
    'NAME': PWMP + 'NumericPasswordValidator'}
]

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.normpath(os.path.abspath(
                    os.path.join(os.path.dirname(__file__),
                                 '..', 'static')))]

INVITE_CODE_LENGTH = 20
assert INVITE_CODE_LENGTH >= 20

PASSWORD_LENGTH = 7
PASSWORD_CHARS = string.ascii_letters + string.digits + '_-=+/!@#$%^&*()[]{}|'
FROM_EMAIL = "inviter@inviter.ru"
EMAIL_USER = os.environ.get('INVITER_EMAIL_USER', 'invalid_user')
EMAIL_PASSWORD = os.environ.get('INVITER_EMAIL_PASSWORD', 'invalid_password')

MAILER = Mailer()
