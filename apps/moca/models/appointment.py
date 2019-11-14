import datetime
from django.db import models
from django.db.models import signals
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.validators import MinValueValidator, MaxValueValidator

from moca.models import Address
from moca.tasks import send_appt_start_notification


class Appointment(models.Model):
  STATUSES = [('in-progress', 'In Progress'), ('not-started', 'Not Started'),
              ('completed', 'Completed'), ('cancelled', 'Cancelled')]

  patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
  therapist = models.ForeignKey('Therapist', on_delete=models.CASCADE)
  address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  start_time_expected = models.DateTimeField(blank=True, null=True)
  end_time_expected = models.DateTimeField(blank=True, null=True)
  status = models.CharField(max_length=15, choices=STATUSES, default='not-started')
  price = models.IntegerField(validators=[MinValueValidator(0)])
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now_add=True)


def appt_start_notification(instance, *args, **kwargs):
  appointment = instance
  appointment_id = appointment.id
  therapist_id = appointment.therapist_id
  patient_id = appointment.patient_id

  notification_time = appointment.start_time - datetime.timedelta(minutes=30)
  # Uncomment for testing celery and notifications
  # notification_time = appointment.created_at + datetime.timedelta(seconds=10)

  send_appt_start_notification.apply_async((appointment_id, therapist_id, patient_id),
                                           eta=notification_time)


signals.post_save.connect(appt_start_notification, sender=Appointment)


class AppointmentRequest(models.Model):
  STATUSES = [('accepted', 'Accepted'), ('rejected', 'Rejected'), ('pending', 'Pending'),
              ('cancelled', 'Cancelled')]

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
  patient = models.ForeignKey('Patient', on_delete=models.CASCADE, related_name='reviews')
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
  files = ArrayField(models.FileField(), blank=True, null=True)


class AppointmentCancellation(models.Model):
  STANDARD = "standard"
  RESCHEDULE = "reschedule"
  WEATHER = "weather"
  EMERGENCY = "emergency"

  CANCELLATION_TYPES = [
    (STANDARD, "Standard Cancellation Policy"),
    (RESCHEDULE, "Rescheduling"),
    (WEATHER, "Cancellation Due to Weather"),
    (EMERGENCY, "Cancellation Due to an Emergency"),
  ]

  appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  is_processed = models.BooleanField(default=False)
  type = models.CharField(max_length=10, choices=CANCELLATION_TYPES)
  cancellation_time = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"Appointment cancellation: {self.id} type: {self.type}"


def validate_appointment_cancellation_type(sender, instance, **kwargs):
  valid_types = [t[0] for t in sender.CANCELLATION_TYPES]
  if instance.type not in valid_types:
    from django.core.exceptions import ValidationError
    raise ValidationError("Unsupported cancellation type")


models.signals.pre_save.connect(validate_appointment_cancellation_type,
                                sender=AppointmentCancellation)
