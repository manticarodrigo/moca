from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import APIException
from django.db import transaction

from moca.models import Conversation, Message, TextMessage, ImageMessage
from moca.api.user.serializers import UserSnippetSerializer


class TextMessageSerializer(serializers.ModelSerializer):
  class Meta:
    model = TextMessage
    fields = ['content']


class ImageMessageSerializer(serializers.ModelSerializer):
  class Meta:
    model = ImageMessage 
    fields = ['content']


class MessageSerializer(serializers.ModelSerializer):
  text = TextMessageSerializer(required=False)
  image = ImageMessageSerializer(required=False)
  user = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = Message
    fields = ['type', 'created_at', 'text', 'image', 'user']

  @transaction.atomic
  def create(self, validated_data):
    request = self.context['request']
    user_id = request.user.id
    target_user_id = self.context.get('view').kwargs.get('user_id')
    type = validated_data.get('type')
    
    if (type not in validated_data):
      raise APIException('No message')

    conversation = Conversation.objects \
                  .filter(participants__id=user_id) \
                  .filter(participants__id=target_user_id).first()

    if not conversation:
      conversation = Conversation()
      conversation.save()
      conversation.participants.add(user_id, target_user_id)

    message = Message.objects.create(conversation=conversation, type=type, user_id=user_id)

    if (type == 'text'):
      TextMessage.objects.create(message=message, **validated_data[type])
    
    
    return message


# class MessageCreateSerializer

# class AppointmentMessageSerializer(serializers.ModelSerializer):
#   type = serializers.CharField(read_only=True)

#   class Meta:
#     model = AppointmentMessage
#     fields = '__all__'


# class MediaMessageSerializer(serializers.ModelSerializer):
#   type = serializers.CharField(read_only=True)

#   class Meta:
#     model = MediaMessage
#     fields = '__all__'


# class UserSerializer(serializers.ModelSerializer):
#   class Meta:
#     model = User
#     fields = ("username", "id")


class ConversationSerializer(serializers.ModelSerializer):
  participants = UserSnippetSerializer(many=True)

  class Meta:
    model = Conversation
    fields = ['participants']

  def to_representation(self, obj):
    user = self.context['request'].user
    representation = super().to_representation(obj)
    participants = representation.pop('participants');
    other_user = next(d for d in participants if d['id'] != user.id)
    last_message = None
    try: 
      last_message = Message.objects.filter(conversation=obj).latest('created_at')
      last_message = MessageSerializer(last_message).data
    except:
      pass

    response = {"user": other_user, "last_message": last_message}
    return response


# class TherapistSearchSerializer(serializers.ModelSerializer):
#   user = UserSnippetSerializer()
#   prices = PriceSerializer(source='tariffs', many=True)

#   class Meta:
#     model = Therapist
#     fields = ['license_number', 'rating', 'user', 'prices'] 

#   def to_representation(self, obj):
#     representation = super().to_representation(obj)
#     user_representation = representation.pop('user')
#     for key in user_representation:
#         representation[key] = user_representation[key]

#     return representation
