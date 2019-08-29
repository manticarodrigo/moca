from django.contrib.auth.models import User
from rest_framework import serializers

from moca.models import Conversation, Message, Participant


class ParticipantSerializer(serializers.ModelSerializer):
  class Meta:
    model = Participant
    fields = '__all__'


class MessageSerializer(serializers.ModelSerializer):
  class Meta:
    model = Message
    fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ("username", "id")


class ConversationSerializer(serializers.ModelSerializer):
  participant_set = ParticipantSerializer(many=True)

  class Meta:
    model = Conversation
    fields = '__all__'
