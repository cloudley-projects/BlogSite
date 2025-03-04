"""
Django settings for blog project.

Generated by 'django-admin startproject' using Django 3.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
import logging

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)

# Create the loggers object
logger = logging.getLogger('__name__')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = os.environ.get('SECRET_KEY','l31o(vihv8z5r*rkgp(8v3&bkou%60tda3f3($wm0_y@zuc9@$')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', True)

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'webapp',
    'cloudtasks',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    #'csp.middleware.CSPMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
SESSION_ENGINE='django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_AGE=1800
ROOT_URLCONF = 'blog.urls'
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'webapp/templates/webapp')],
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

WSGI_APPLICATION = 'blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

if os.environ.get('DB_TYPE') == 'cloudsql':
    DATABASES = {
        'default': {
            'ENGINE'  : 'mysql.connector.django', # <-- UPDATED line 
            'NAME'    : os.environ['DB_NAME'],              # <-- UPDATED line 
            'USER'    : os.environ['DB_USER'],                     # <-- UPDATED line
            'PASSWORD': os.environ['DB_PASSWORD'],              # <-- UPDATED line
            'HOST'    : os.environ['DB_HOST'],                # <-- UPDATED line
            'PORT'    : os.environ['DB_PORT']
        }
    }
    logger.warning('Environment variable is set and CloudSQL database is being used')
    
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
    logger.warning('Environment variable is not set and default database is being used')

# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATICFILES_DIRS = [
#   os.path.join(BASE_DIR, 'static')
]
STATIC_ROOT = "static"
STATIC_URL = "/static/"


#CSP
#CSP_DEFAULT_SRC = ("'self'", 'cdn.example.net')
#CSP_CONNECT_SRC = ("'self'", 'https://www.googleapis.com/identitytoolkit/v3/', 'https://securetoken.googleapis.com/v1/')
#CSP_IMG_SRC = ("'self'", 'https://html.sammy-codes.com','https: data:' )
#CSP_STYLE_SRC = ("'self'", 'https://fonts.googleapis.com', 'https://cdn.jsdelivr.net/')
#CSP_SCRIPT_SRC = ("'self'",'https://cdn.jsdelivr.net/')
#CSP_BASE_URI = ("'self'")
#CSP_OBJECT_URI = ("'self'")
#CSP_FONT_SRC = ("'self'", 'https://fonts.gstatic.com/')
#CSP_INCLUDE_NONCE_IN = ['script-src']