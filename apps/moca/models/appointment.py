from django.db import models
from django.contrib.postgres.fields import ArrayField

from moca.models import Address
from moca.models.user import Patient, Therapist


class Appointment(models.Model):
  patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
  therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE)
  address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  start_time_expected = models.DateTimeField(blank=True, null=True)
  end_time_expected = models.DateTimeField(blank=True, null=True)
  is_cancelled = models.BooleanField(default=False)
  price = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
  appointment = models.ForeignKey(Appointment,
                                  on_delete=models.CASCADE,
                                  related_name='review',
                                  primary_key=False)
  rating = models.FloatField()
  comment = models.CharField(blank=True, null=True, max_length=200)

class Note(models.Model):
  appointment = models.ForeignKey(Appointment,
                                  on_delete=models.CASCADE,
                                  related_name='note',
                                  primary_key=False)
  subjective = models.TextField(blank=True)
  objective = models.TextField(blank=True)
  treatment = models.TextField(blank=True)
  assessment = models.TextField(blank=True)
  diagnosis = models.TextField(blank=True)
  files = ArrayField(models.FileField())
