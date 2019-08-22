from django.db import models
from django.conf import settings
from django.contrib.gis.db import models as gisModels

class Address(models.Model):
    name = models.CharField(max_length=50)
    street = models.CharField(max_length=50)
    zip_code = models.SmallIntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    primary = models.BooleanField()
    apartment = models.CharField(max_length=50)
    location = gisModels.PointField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
