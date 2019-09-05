from django.contrib.auth.models import User
from rest_framework import serializers

from moca.models import (AttachmentMessage, Conversation, Message,
                         RequestMessage, ResponseMessage, TextMessage)


class MessageSerializer(serializers.ModelSerializer):
  class Meta:
    model = Message
    fields = '__all__'


class RequestSerializer(serializers.ModelSerializer):
  type = serializers.CharField(read_only=True)

  class Meta:
    model = RequestMessage
    fields = '__all__'


class ResponseSerializer(serializers.ModelSerializer):
  type = serializers.CharField(read_only=True)

  class Meta:
    model = ResponseMessage
    fields = '__all__'


class TextMessageSerializer(serializers.ModelSerializer):
  type = serializers.CharField(read_only=True)

  class Meta:
    model = TextMessage
    fields = '__all__'


class AttachmentSerializer(serializers.ModelSerializer):
  type = serializers.CharField(read_only=True)

  class Meta:
    model = AttachmentMessage
    fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ("username", "id")


class ConversationSerializer(serializers.ModelSerializer):
  class Meta:
    model = Conversation
    fields = '__all__'
