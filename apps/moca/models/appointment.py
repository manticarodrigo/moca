import datetime
from django.db import models
from django.db.models import signals
from django.utils import timezone
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

from .user.address import Address


class Appointment(models.Model):
  STATUSES = [('in-progress', 'In Progress'), ('not-started', 'Not Started'),
              ('completed', 'Completed'), ('cancelled', 'Cancelled'),
              ('payment-failed', 'Payment Failed')]

  patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
  therapist = models.ForeignKey('Therapist', on_delete=models.CASCADE)
  address = models.ForeignKey(Address, on_delete=models.DO_NOTHING)
  start_time = models.DateTimeField()
  end_time = models.DateTimeField()
  start_time_manual = models.DateTimeField(blank=True, null=True)
  end_time_manual = models.DateTimeField(blank=True, null=True)
  status = models.CharField(max_length=15, choices=STATUSES, default='not-started')
  price = models.IntegerField(validators=[MinValueValidator(0)])
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now_add=True)


def post_save_appointment(instance, *args, **kwargs):
  from moca.tasks import (send_appt_upcoming_notification, send_appt_start_notification,
                          send_appt_review_notification)
  appointment = instance
  appointment_id = appointment.id

  upcoming_notification_time = appointment.start_time - datetime.timedelta(minutes=30)
  start_notification_time = (appointment.start_time_manual if appointment.start_time_manual and
                              appointment.start_time > appointment.start_time_manual else
                              appointment.start_time)
  review_notification_time = (appointment.end_time_manual if appointment.end_time_manual and
                              appointment.end_time > appointment.end_time_manual else
                              appointment.end_time)

  if upcoming_notification_time > timezone.now():
    send_appt_upcoming_notification.apply_async((appointment_id, ), eta=upcoming_notification_time)

  send_appt_start_notification.apply_async((appointment_id, ), eta=start_notification_time)
  send_appt_review_notification.apply_async((appointment_id, ), eta=review_notification_time)


signals.post_save.connect(post_save_appointment, sender=Appointment)


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
  appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name="note")
  subjective = models.TextField(blank=True)
  objective = models.TextField(blank=True)
  treatment = models.TextField(blank=True)
  assessment = models.TextField(blank=True)
  diagnosis = models.TextField(blank=True)


class NoteImage(models.Model):
  note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name="images")
  image = models.ImageField(upload_to='notes',)


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
