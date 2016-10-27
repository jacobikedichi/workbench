"""
Django settings for workbench project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
from ConfigParser import RawConfigParser

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
parser = RawConfigParser()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = [] #This is the default when DEBUG is True. Different values are used in different 
                   #environments (i.e. Prodcution, Staging, Testing, Development)
XFRAME_EXEMPT_IPS = [] #All the hostnames that we wish to give permission to load our web content in an iframe

# Application definition

INSTALLED_APPS = [
    #our apps
    'workbench',
    "comments",
    #other 3rd party apps
    'rest_framework', #django-rest-framework
    #django defaults
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'workbench.middleware.ExemptFrameOptionsMiddleware',
]

ROOT_URLCONF = 'workbench.urls'

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

WSGI_APPLICATION = 'workbench.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

env_file = os.path.join(BASE_DIR, ".env")

if not os.path.isfile(env_file):
    #Use django default sqlite db settings
    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'uv*p&wv5wwcvuv6m$uc_j56-!x7!%%0m_yp9v#j(^ku!##6(^='
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    parser.read(env_file)

    ALLOWED_HOSTS = parser.get('general', 'ALLOWED_HOSTS').split(',')
    SECRET_KEY = parser.get('general', 'SECRET_KEY')
    DEBUG = parser.getboolean('general', 'DEBUG')
    #We need to filter out all empty values in the list
    XFRAME_EXEMPT_IPS = filter(None, parser.get('general', 'XFRAME_EXEMPT_IPS').split(','))
    DATABASES = {
        'default': {
            'ENGINE': parser.get('database', 'DB_ENGINE'),
            'NAME': parser.get('database', 'DB_NAME'),
            'USER': parser.get('database', 'DB_USER'),
            'PASSWORD': parser.get('database', 'DB_PASSWORD'),
            'HOST': parser.get('database', 'DB_HOST'),
            'PORT': parser.get('database', 'DB_PORT'),
        }
    }

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
#     'DEFAULT_PERMISSION_CLASSES': [
#         'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
#     ],
    'DEFAULT_AUTHENTICATION_CLASSES': [], #Dont worry about these for now
    'DEFAULT_PERMISSION_CLASSES': [],
    
    'DEFAULT_THROTTLE_CLASSES': (
        'comments.throttling.CommentCreateRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ),
    'DEFAULT_THROTTLE_RATES': {
        'create_comment': '2/minute',
        'anon': '20/minute',
        'user': '20/minute'
    },
}

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'var', 'static')
