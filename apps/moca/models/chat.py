from django.db import models
from django.conf import settings


class Conversation(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)

  def __str__(self):
    return f"conversation {self.id}"


# TODO move this inside conversation as a ArrayField in Conversation
class Participant(models.Model):
  conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

  def __str__(self):
    return f"{self.user} in {self.conversation}"


class Message(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE)
  text = models.TextField()

  def __str__(self):
    return f"'{self.text}' by {self.user} in {self.conversation}"
