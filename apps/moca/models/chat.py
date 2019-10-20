from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.db.models.signals import m2m_changed
from django.core.exceptions import ValidationError

from moca.models.appointment import Appointment


class Conversation(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='participants')

  def __str__(self):
    return f"conversation {self.id}"

def participants_changed(sender, **kwargs):
  if kwargs['instance'].participants.count() > 3:
    raise ValidationError("You can't assign more than three participants")


m2m_changed.connect(participants_changed, sender=Conversation.participants.through)


class Message(models.Model):
  MESSAGE_TYPE_TEXT = 'text'
  PAYMENT_TYPE_IMAGE = 'image'
  MESSAGE_TYPES = [(MESSAGE_TYPE_TEXT, 'Text'), (PAYMENT_TYPE_IMAGE, 'Image')]

  conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True)
  type = models.CharField(max_length=15, choices=MESSAGE_TYPES)


class TextMessage(models.Model):
  message = models.OneToOneField(Message, related_name="text", on_delete=models.CASCADE)
  content = models.TextField()
  
  
class ImageMessage(models.Model):
  message = models.OneToOneField(Message, related_name="image", on_delete=models.CASCADE)
  content = models.FileField()

# class MediaMessage(models.Model):
#   message = models.OneToOneField(Message, on_delete=models.CASCADE)
#   type = MessageTypes.MEDIA
#   text = models.TextField(null=True)
#   file = models.FileField(null=True)
#   MEDIA_TYPES = [('application/pdf', 'pdf'), ('image/jpg', 'jpg'), ('image/png', 'png')]
#   mediaType = models.CharField(max_length=10, choices=MEDIA_TYPES)


# class AppointmentMessage(models.Model):
#   message = models.OneToOneField(Message, on_delete=models.CASCADE)
#   type = MessageTypes.REQUEST
#   RESPONSE_TYPES = [('Accepted', 'Accepted'), ('Rejected', 'Rejected')]
#   appointment = models.ForeignKey(Appointment, on_delete=models.PROTECT, related_name='messages')
#   response = models.CharField(max_length=10, choices=RESPONSE_TYPES, null=True)
