import os

import dj_database_url

from .base import *

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Secret key for the dev environment
SECRET_KEY = os.environ['MOCA_SECRET']

db_from_env = dj_database_url.config()
DATABASES['default'] = db_from_env
