from django.db import models


class AvailableArea(models.Model):
  state = models.CharField(max_length=2)


class UnavailableArea(models.Model):
  email = models.EmailField()
  state = models.CharField(max_length=2)
