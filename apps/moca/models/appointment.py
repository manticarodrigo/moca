from django.db import models

from moca.models import User, Address
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
  notes = models.CharField(max_length=200, blank=True, null=True)
  price = models.IntegerField()
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
  appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
  rating = models.IntegerField()
  comment = models.CharField(blank=True, null=True, max_length=200)
