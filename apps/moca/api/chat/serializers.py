from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import APIException
from django.db import transaction

from moca.models import Conversation, Message, TextMessage, ImageMessage, AppointmentRequest, \
  AppointmentRequestMessage
from moca.api.user.serializers import UserSnippetSerializer
from moca.api.appointment.serializers import AppointmentRequestSerializer, \
  AppointmentRequestCreateSerializer


class TextMessageSerializer(serializers.ModelSerializer):
  class Meta:
    model = TextMessage
    fields = ['text']


class ImageMessageSerializer(serializers.ModelSerializer):
  class Meta:
    model = ImageMessage 
    fields = ['content']


class AppointmentRequestMessageSerializer(serializers.ModelSerializer):
  appointment_request = AppointmentRequestSerializer()

  class Meta:
    model = AppointmentRequestMessage
    fields = ['appointment_request']

  def to_representation(self, obj):
      representation = super().to_representation(obj)
      return representation["appointment_request"]


class MessageSerializer(serializers.ModelSerializer):
  user = serializers.PrimaryKeyRelatedField(read_only=True)
  content = serializers.SerializerMethodField(required=False)

  class Meta:
    model = Message
    fields = ['type', 'created_at', 'user', 'content']

  def get_content(self, obj):
    message_type = obj.type
    if message_type == 'appointment-request':
      appointment_request_message = AppointmentRequestMessage.objects.get(message=obj)
      return AppointmentRequestMessageSerializer(appointment_request_message).data
    elif message_type == 'text':
      text_message = TextMessage.objects.get(message=obj)
      return TextMessageSerializer(text_message).data
    else:
      raise APIException('Invalid message content')

  @transaction.atomic
  def create(self, validated_data):
    request = self.context['request']
    user_id = request.user.id
    target_user_id = self.context.get('view').kwargs.get('user_id')
    type = validated_data.get('type')
    content = request.data.get('content')
    
    if not content:
      raise APIException('No message content')

    conversation = Conversation.objects \
                  .filter(participants__id=user_id) \
                  .filter(participants__id=target_user_id).first()

    if not conversation:
      conversation = Conversation()
      conversation.save()
      conversation.participants.add(user_id, target_user_id)

    message = Message.objects.create(conversation=conversation, type=type, user_id=user_id)

    if (type == 'text'):
      TextMessage.objects.create(message=message, **content)
    
    elif (type == 'appointment-request'):
      appointment_request_serializer = AppointmentRequestCreateSerializer(data=content, context={'request': request})
      if (appointment_request_serializer.is_valid()):
        appointment_request = appointment_request_serializer.save()
      else:
        raise APIException('Invalid request message')

      AppointmentRequestMessage.objects.create(message=message, appointment_request=appointment_request)
    else:
      raise APIException('Invalid message type')
    
    return message


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
