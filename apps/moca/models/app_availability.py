from django.db import models


class Area(models.Model):
  state = models.CharField(max_length=2)
  zip_code = models.CharField(max_length=5)
