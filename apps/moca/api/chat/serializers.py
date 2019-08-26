from rest_framework import serializers
from django.contrib.auth.models import User

from moca.models import Conversation, Message


class MessageSerializer(serializers.ModelSerializer):
  class Meta:
    model = Message
    fields = ("text", "created_at", "user")


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ("username", "id")
