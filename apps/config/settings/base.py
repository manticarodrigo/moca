"""
Django settings for moca project.

Generated by 'django-admin startproject' using Django 2.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import os

AUTH_USER_MODEL = 'moca.User'

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = [
  # Django
  'fcm_django',
  'django.contrib.admin',
  'django.contrib.auth',
  'django.contrib.contenttypes',
  'django.contrib.sessions',
  'django.contrib.messages',
  'django.contrib.staticfiles',
  'django.contrib.gis',
  # 3rd party
  'rest_framework',
  'corsheaders',
  'knox',
  'rest_framework_gis',
  # Apps
  'moca.apps.MocaConfig',
]
LOGGING = {
  'version': 1,
  'filters': {
    'require_debug_true': {
      '()': 'django.utils.log.RequireDebugTrue',
    }
  },
  'handlers': {
    'console': {
      'level': 'DEBUG',
      'filters': ['require_debug_true'],
      'class': 'logging.StreamHandler',
    }
  },
  'loggers': {
    'django.db.backends': {
      'level': 'DEBUG',
      'handlers': ['console'],
    }
  }
}

REST_FRAMEWORK = {
  # Rest framework settings
  'DEFAULT_AUTHENTICATION_CLASSES': ('knox.auth.TokenAuthentication', ),
  'DEFAULT_PERMISSION_CLASSES': [
    # 'rest_framework.permissions.IsAuthenticated',
  ],
  'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
  'PAGE_SIZE': 10,
  'DEFAULT_RENDERER_CLASSES': ('djangorestframework_camel_case.render.CamelCaseJSONRenderer', ),
  'DEFAULT_PARSER_CLASSES': ('djangorestframework_camel_case.parser.CamelCaseJSONParser', ),
}

MIDDLEWARE = [
  'django.middleware.security.SecurityMiddleware',
  'django.contrib.sessions.middleware.SessionMiddleware',
  'corsheaders.middleware.CorsMiddleware',
  'django.middleware.common.CommonMiddleware',
  'django.middleware.csrf.CsrfViewMiddleware',
  'django.contrib.auth.middleware.AuthenticationMiddleware',
  'django.contrib.messages.middleware.MessageMiddleware',
  'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
# APPEND_SLASH=False

FCM_DJANGO_SETTINGS = {
  "APP_VERBOSE_NAME": "LoyalSpots",
  # default: _('FCM Django')
  "FCM_SERVER_KEY": "AIzaSyD - jU8Bh5L9BRYpBLlz - 9v2EElcy_3sxYs",
  # true if you want to have only one active device per registered user at a time
  # default: False
  "ONE_DEVICE_PER_USER": False,
  # devices to which notifications cannot be sent,
  # are deleted upon receiving error response from FCM
  # default: False
  "DELETE_INACTIVE_DEVICES": False,
}

FCM_DJANGO_SETTINGS.setdefault("USER_MODEL", AUTH_USER_MODEL)
