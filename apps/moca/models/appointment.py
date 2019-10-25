from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator

from moca.models import Address


class Appointment(models.Model):
  patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
  therapist = models.ForeignKey('Therapist', on_delete=models.CASCADE)
  address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  start_time_expected = models.DateTimeField(blank=True, null=True)
  end_time_expected = models.DateTimeField(blank=True, null=True)
  is_cancelled = models.BooleanField(default=False)
  price = models.IntegerField(validators=[MinValueValidator(0)])
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now_add=True)


class AppointmentRequest(models.Model):
  STATUSES = [('accepted', 'Accepted'), ('rejected', 'Rejected'), ('pending', 'Pending')]

  appointment = models.ForeignKey(Appointment,
                                  related_name="appointment",
                                  on_delete=models.DO_NOTHING,
                                  null=True)
  status = models.CharField(max_length=10, choices=STATUSES, default='pending')
  patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
  therapist = models.ForeignKey('Therapist', on_delete=models.CASCADE)
  address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  price = models.IntegerField(validators=[MinValueValidator(0)])
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now_add=True)


class Review(models.Model):
  therapist = models.ForeignKey('Therapist', on_delete=models.CASCADE, related_name='reviews')
  appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
  rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)])
  comment = models.TextField(blank=True)


class Note(models.Model):
  appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
  subjective = models.TextField(blank=True)
  objective = models.TextField(blank=True)
  treatment = models.TextField(blank=True)
  assessment = models.TextField(blank=True)
  diagnosis = models.TextField(blank=True)
  files = ArrayField(models.FileField())
