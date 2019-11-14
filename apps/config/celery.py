from __future__ import absolute_import, unicode_literals
import os, sys
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

sys.path.append(os.path.abspath('config'))
app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
  print('Request: {0!r}'.format(self.request))
