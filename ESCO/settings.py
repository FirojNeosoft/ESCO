"""
Django settings for ESCO project.

Generated by 'django-admin startproject' using Django 2.1.4.

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
SECRET_KEY = 'skr@7vxa!oc+537!ti#ekg^*r@-^t_1!_*wj*+7a6=oq2)&6hp'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export',
    'CMS',
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

ROOT_URLCONF = 'ESCO.urls'

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

WSGI_APPLICATION = 'ESCO.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'ESCO',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost'
    }
}

# DATABASES = {
#     'default': {
#         'ENGINE': 'sql_server.pyodbc',
#         'NAME': 'ESCO_CMS',
#         'USER': '',
#         'PASSWORD': '',
#         'HOST': '166.62.119.178\SQLEXPRESS2014',
#         'PORT': '11433',
#         'OPTIONS': {
#             'driver': 'ODBC Driver 17 for SQL Server',
#         },
#     }
# }

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

DATE_INPUT_FORMATS = ('%m-%d-%Y')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "base_static"),
)

# MEDIA files
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# Logs configuration
LOG_ROOT = os.path.join(BASE_DIR, 'docs/logs/')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'null': {
            'class': 'logging.NullHandler',
        },
        'cms_log_file': {
            'level': 'DEBUG',
            'filters': ['require_debug_true'],
            'formatter': 'verbose',
            'class': 'logging.FileHandler',
            'filename': LOG_ROOT+'cms.log',
        },
    },
    'loggers': {
        'cms_log': {
            'handlers': ['cms_log_file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
    },
}

# Required choices variables
GENDER_CHOICES = (('M', 'Male'), ('F', 'Female'))
STATUS_CHOICES = (('Active', 'Active'), ('Inactive', 'Inactive'), ('Delete', 'Delete'))
BINARY_CHOICES = (('Yes', 'Yes'), ('No', 'No'))
ACCOUNT_TYPE = (('New Customer', 'New Customer'), ('Renewal', 'Renewal'))
SBC = (('Yes', 'Yes'),)
CUSTOMER_TYPE = (('Commercial', 'Commercial'), ('Residential', 'Residential'), ('Industrial', 'Industrial'),\
                 ('Religious', 'Religious'), ('Anders', 'Anders'))
BILLING = (('POR', 'POR'), ('DUAL', 'DUAL'))
PASSTHRU = (('GRT', 'GRT'), ('REC/ZEC', 'REC/ZEC'), ('ICAP', 'ICAP'), ('TRANS', 'TRANS'), ('OPTION5', 'OPTION5'),\
            ('OPTION6', 'OPTION6'))
RATE_CLASS = (('OPTION1', 'OPTION1'), ('OPTION2', 'OPTION2'), ('OPTION3', 'OPTION3'), ('OPTION4', 'OPTION4'), ('OPTION5', 'OPTION5'),\
            ('OPTION6', 'OPTION6'))
ELECTRIC_UTILITY = (('ConEdison', 'ConEdison'), ('PSEG-LIPA', 'PSEG-LIPA'), ('National Grid', 'National Grid'), ('NYSEG', 'NYSEG'), ('RGE', 'RGE'),\
            ('CHUD', 'CHUD'), ('OPTION7', 'OPTION7'), ('OPTION8', 'OPTION8'))
GAS_UTILITY = (('ConEdison', 'ConEdison'), ('PSEG-LIPA', 'PSEG-LIPA'), ('National Grid', 'National Grid'), ('NYSEG', 'NYSEG'), ('RGE', 'RGE'),\
            ('CHUD', 'CHUD'), ('OPTION7', 'OPTION7'), ('OPTION8', 'OPTION8'))
UTILITY_ACCOUNT_TYPE = (('OPTION1', 'OPTION1'), ('OPTION2', 'OPTION2'), ('OPTION3', 'OPTION3'))
DELIVERY_TYPE = (('Firm', 'Firm'), ('Interruptible', 'Interruptible'))
PRICE_PLAN = (('Fixed', 'Fixed'), ('Variable', 'Variable'), ('Index', 'Index'))
ZONE = (('Zone A', 'Zone A'), ('Zone B', 'Zone B'), ('Zone C', 'Zone C'), ('Zone D', 'Zone D'), ('Zone E', 'Zone E'), \
        ('Zone F', 'Zone F'), ('Zone G', 'Zone G'), ('Zone H', 'Zone H'), ('Zone I', 'Zone I'), ('Zone J', 'Zone J'), \
        ('Zone K', 'Zone K'), ('PSEG', 'PSEG'), ('JCPL', 'JCPL'), ('ACEC', 'ACEC'), ('DPL', 'DPL'))

# config for django-import-export package
IMPORT_EXPORT_USE_TRANSACTIONS = True

