from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models

from moca.models.appointment import Appointment


class MessageTypes:
  MEDIA = "media"
  REQUEST = "request"
  RESPONSE = "response"


class Conversation(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='participants')

  def __str__(self):
    return f"conversation {self.id}"


class Message(models.Model):
  conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  type = None

  class Meta:
    abstract = True


class MediaMessage(Message):
  type = MessageTypes.MEDIA
  text = models.TextField(null=True)
  file = models.FileField(null=True)
  MEDIA_TYPES = [('application/pdf', 'pdf'), ('image/jpg', 'jpg'), ('image/png', 'png')]
  mediaType = models.CharField(max_length=10, choices=MEDIA_TYPES)


class AppointmentMessage(Message):
  type = MessageTypes.REQUEST
  RESPONSE_TYPES = [('Accepted', 'Accepted'), ('Rejected', 'Rejected')]
  appointment = models.ForeignKey(Appointment, on_delete=models.PROTECT, related_name='messages')
  response = models.CharField(max_length=10, choices=RESPONSE_TYPES, null=True)
