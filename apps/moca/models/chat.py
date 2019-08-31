from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.db import models


class MessageTypes:
  REQUEST = "request"
  RESPONSE = "response"
  ATTACHMENT = "attachment"
  TEXT = "text"


class Conversation(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='participants')

  def __str__(self):
    return f"conversation {self.id}"


class Message(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
  type = None

  class Meta:
    abstract = True


class TextMessage(Message):
  type = MessageTypes.TEXT
  text = models.TextField()


# TODO maybe this should be just appointment request which
# will contain a date and two choices accept or reject
# rather than an array of options
class RequestMessage(Message):
  type = MessageTypes.REQUEST
  options = ArrayField(models.TextField())


class ResponseMessage(Message):
  type = MessageTypes.RESPONSE
  selection = models.IntegerField()
  reply_to = models.ForeignKey(RequestMessage, on_delete=models.PROTECT)


class AttachmentMessage(Message):
  type = MessageTypes.ATTACHMENT
  # TODO check this versus ImageField
  url = models.FileField()
