from .base import *

DEBUG = True

# Secret key for the dev environment
SECRET_KEY = 'fi_nlfw&)!t_ep1c$q435a+!)q*8a4kr$b_#w#j5gj!2#0q^5n'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
  'default': {
    'ENGINE': 'django.contrib.gis.db.backends.postgis',
    'NAME': 'moca_db',
    'USER': 'moca_user',
    'PASSWORD': 'moca_password',
    'HOST': 'moca_db',  # set in docker-compose.yml
    'PORT': 5432
  }
}

ALLOWED_HOSTS = ['*']
