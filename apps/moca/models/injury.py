from django.db import models
from django.contrib.postgres.fields import ArrayField

from moca.models.user import Patient 


class Injury(models.Model):
  patient = models.OneToOneField(Patient, on_delete=models.CASCADE)
  title = models.CharField(max_length=50)
  description = models.TextField()
  images = ArrayField(models.ImageField(upload_to='injuries'), null=True)