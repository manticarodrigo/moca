from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import m2m_changed


class Conversation(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='participants')

  def __str__(self):
    return f"conversation {self.id}"


def participants_changed(sender, **kwargs):
  if kwargs['instance'].participants.count() > 3:
    raise ValidationError("You can't assign more than three participants")


m2m_changed.connect(participants_changed, sender=Conversation.participants.through)


class LastViewed(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
  timestamp = models.DateTimeField()


class Message(models.Model):
  MESSAGE_TYPE_COMPOSITE = 'composite'
  MESSAGE_TYPE_APPOINTMENT_REQUEST = 'appointment-request'
  MESSAGE_TYPES = [(MESSAGE_TYPE_COMPOSITE, 'Composite'),
                   (MESSAGE_TYPE_APPOINTMENT_REQUEST, 'Appointment Request')]

  conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  type = models.CharField(max_length=20, choices=MESSAGE_TYPES)


class CompositeMessage(models.Model):
  message = models.OneToOneField(Message, on_delete=models.CASCADE)
  title = models.CharField(max_length=50, null=True)
  text = models.TextField()


class CompositeMessageImage(models.Model):
  message = models.ForeignKey(CompositeMessage, related_name="images", on_delete=models.CASCADE)
  image = models.ImageField(upload_to="messages")


class AppointmentRequestMessage(models.Model):
  message = models.OneToOneField(Message, on_delete=models.CASCADE)
  appointment_request = models.OneToOneField('AppointmentRequest',
                                             related_name="appointment_request",
                                             on_delete=models.DO_NOTHING)
