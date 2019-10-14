from django.contrib.auth.models import User
from rest_framework import serializers

from moca.models import (Conversation, Message, MediaMessage, AppointmentMessage)
from moca.models.chat import MediaMessage


class MessageSerializer(serializers.ModelSerializer):
  class Meta:
    model = Message
    fields = '__all__'


class AppointmentMessageSerializer(serializers.ModelSerializer):
  type = serializers.CharField(read_only=True)

  class Meta:
    model = AppointmentMessage
    fields = '__all__'


class MediaMessageSerializer(serializers.ModelSerializer):
  type = serializers.CharField(read_only=True)

  class Meta:
    model = MediaMessage
    fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ("username", "id")


class ConversationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Conversation
    fields = '__all__'
