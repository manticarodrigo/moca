from django.db import models


class Area(models.Model):
  zip_code = models.CharField(max_length=5)


class UnavailableArea(models.Model):
  email = models.EmailField()
  zip_code = models.CharField(max_length=5)
