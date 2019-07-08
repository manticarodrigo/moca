import os
import dj_database_url
import django_heroku

from .base import *

# Secret key for the dev environment
SECRET_KEY = os.environ['MOCA_SECRET']

db_from_env = dj_database_url.config()
DATABASES['default'] = db_from_env

# Configure Django App for Heroku.
django_heroku.settings(locals())