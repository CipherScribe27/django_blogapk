"""
Django settings for django_project project.

Generated by 'django-admin startproject' using Django 2.1.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'exhlfdat&vfum(-34*c2uroi(($ww(yo$9pv98=e6p^gl(-eoj'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'blog.apps.BlogConfig',
    'users.apps.UsersConfig',
    'crispy_forms',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'admin_honeypot',
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

ROOT_URLCONF = 'django_project.urls'

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

WSGI_APPLICATION = 'django_project.wsgi.application'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = 'blog-home'
LOGIN_URL = 'login'

# from dotenv import load_dotenv
# load_dotenv()

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'ansarimohamed07.uniq@gmail.com'  # Enter your Gmail address
EMAIL_HOST_PASSWORD = 'ymeo inzs rnuh sjzo'  # Enter your Gmail password or app-specific password if 2-factor authentication is enabled


# EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
# EMAIL_HOST_USER = os.environ.get('EMAIL_USER')
# EMAIL_HOST_USER = os.environ.get('EMAIL_PASS')

# EMAIL_HOST_USER = os.environ.get('USER_EMAIL')
# EMAIL_HOST_PASSWORD = "blnm bdyu sbgs tzcl"
# EMAIL_HOST_PASSWORD = os.environ.get('USER_PASS')


# EMAIL_HOST = 'smpt.gmail.com'

# EMAIL_PORT = '587'

# EMAIL_HOST_USER = [os.environ.get("EMAIL_HOST_USE")]

# EMAIL_HOST_PASSWORD = [os.environ.get("EMAIL_HOST_PASSWOR")]

# EMAIL_USE_TLS = True




from django.core.mail import mail_admins
from django.core.mail import get_connection
from django.core.cache import cache
from django.conf import settings
import datetime

def check_smtp_validity():
    last_check_timestamp = cache.get('last_smtp_check_timestamp')
    current_time = datetime.datetime.now()

    # Check if the last check timestamp exists and if it's within 7 days
    if last_check_timestamp and (current_time - last_check_timestamp).days < 7:
        # Return True to indicate that SMTP is considered valid (since it was checked recently)
        return True, None

    try:
        connection = get_connection(
            backend='django.core.mail.backends.smtp.EmailBackend',
            host=settings.EMAIL_HOST,
            port=settings.EMAIL_PORT,
            username=settings.EMAIL_HOST_USER,
            password=settings.EMAIL_HOST_PASSWORD,
            use_tls=settings.EMAIL_USE_TLS,
            fail_silently=False,
        )
        connection.open()
        connection.close()

        # Update the last check timestamp in cache
        cache.set('last_smtp_check_timestamp', current_time, timeout=None)

        return True, None
    except Exception as e:
        error_message = f"SMTP configuration is invalid: {str(e)}"
        return False, error_message

# Check SMTP validity
is_valid, error_message = check_smtp_validity()

if not is_valid:
    # SMTP configuration is invalid, send an email to admins
    mail_admins("SMTP Configuration Invalid", error_message)

