from django.conf import settings
from django.contrib.postgres.fields import ArrayField
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
  MESSAGE_TYPE_TEXT = 'text'
  MESSAGE_TYPE_IMAGE = 'image'
  MESSAGE_TYPE_APPOINTMENT_REQUEST = 'appointment-request'
  MESSAGE_TYPES = [(MESSAGE_TYPE_TEXT, 'Text'), (MESSAGE_TYPE_IMAGE, 'Image'),
                   (MESSAGE_TYPE_APPOINTMENT_REQUEST, 'Appointment Request')]

  conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name="messages")
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  type = models.CharField(max_length=20, choices=MESSAGE_TYPES)


class TextMessage(models.Model):
  message = models.OneToOneField(Message, related_name="text", on_delete=models.CASCADE)
  text = models.TextField()


class ImageMessage(models.Model):
  message = models.OneToOneField(Message, related_name="image", on_delete=models.CASCADE)
  image = models.FileField()


class AppointmentRequestMessage(models.Model):
  message = models.OneToOneField(Message, on_delete=models.CASCADE)
  appointment_request = models.OneToOneField('AppointmentRequest',
                                             related_name="appointment_request",
                                             on_delete=models.DO_NOTHING)
