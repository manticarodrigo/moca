from django.contrib.auth.models import User
from django.db import transaction
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.utils.serializer_helpers import BindingDict

from moca.api.appointment.serializers import (AppointmentRequestCreateSerializer,
                                              AppointmentRequestSerializer)
from moca.api.user.serializers import UserSnippetSerializer
from moca.models import (Address, AppointmentRequest, Conversation, Message, CompositeMessage,
                         CompositeMessageImage, AppointmentRequestMessage, LastViewed, Device)
from moca.utils.serializer_helpers import combineSerializers
from moca.services.push import send_push_message


class CompositeMessageImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = CompositeMessageImage
    fields = ['image']


class CompositeMessageSerializer(serializers.ModelSerializer):
  images = CompositeMessageImageSerializer(many=True, read_only=True)

  class Meta:
    model = CompositeMessage
    fields = ['title', 'text', 'images']

class AppointmentRequestMessageSerializer(serializers.ModelSerializer):
  appointment_request = AppointmentRequestSerializer()

  class Meta:
    model = AppointmentRequestMessage
    fields = ['appointment_request']

  def to_representation(self, obj):
    representation = super().to_representation(obj)
    return representation["appointment_request"]


ChatMessageSerializer = combineSerializers(CompositeMessageSerializer,
                                           AppointmentRequestMessageSerializer,
                                           serializerName=lambda a, b: 'ChatMessage')


class MessageSerializer(serializers.ModelSerializer):
  user = serializers.PrimaryKeyRelatedField(read_only=True)
  content = serializers.SerializerMethodField(read_only=False)

  class Meta:
    model = Message
    fields = ['type', 'created_at', 'user', 'content']

  @swagger_serializer_method(serializer_or_field=ChatMessageSerializer)
  def get_content(self, obj):
    message_type = obj.type
    if message_type == 'appointment-request':
      appointment_request_message = AppointmentRequestMessage.objects.get(message=obj)
      return AppointmentRequestMessageSerializer(appointment_request_message).data
    elif message_type == 'composite':
      composite_message = CompositeMessage.objects.get(message=obj)
      return CompositeMessageSerializer(composite_message).data
    else:
      raise APIException('Invalid message content')

  @transaction.atomic
  def create(self, validated_data):
    request = self.context['request']
    user_id = request.user.id
    target_user_id = self.context.get('view').kwargs.get('user_id')
    content = request.data.dict()
    type = content.pop('type')

    if target_user_id == user_id:
      raise APIException('Can\'t message yourself')

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

    if type == 'composite':
      if content.get('images'):
        # TODO: better way to handle this
        content.pop('images')

      composite_message = CompositeMessage.objects.create(message=message, **content)

      images_data = self.context.get('view').request.FILES
      for image_data in images_data.getlist('images'):
        CompositeMessageImage.objects.create(message=composite_message, image=image_data)

    elif type == 'appointment-request':
      content['therapist'] = user_id
      content['patient'] = target_user_id

      try:
        primary_address = Address.objects.get(user_id=content['patient'], primary=True)
        content['address'] = primary_address.id
      except Address.DoesNotExist:
        raise APIException('Patient does not have a primary address')

      appointment_request_serializer = AppointmentRequestCreateSerializer(
        data=content, context={'request': request})
      appointment_request_serializer.is_valid(raise_exception=True)
      appointment_request = appointment_request_serializer.save()

      AppointmentRequestMessage.objects.create(message=message,
                                               appointment_request=appointment_request)
    else:
      raise APIException('Invalid message type')

    
    devices = Device.objects.filter(user=target_user_id)
    text = f'New message from {request.user.first_name} {request.user.last_name}.'

    for device in devices:
      send_push_message(device.token, text, {
        'type': 'new_message',
        'params': {
          'user': {
            'id': user_id
          }
        }
      })

    return message


class ConversationSerializer(serializers.ModelSerializer):
  other_user = serializers.SerializerMethodField()
  last_message = serializers.SerializerMethodField()
  unread_count = serializers.SerializerMethodField()

  class Meta:
    model = Conversation
    fields = ['other_user', 'last_message', 'unread_count']

  def get_unread_count(self, obj):
    user = self.context['request'].user

    try:
      last_viewed_timestamp = LastViewed.objects.get(user=user, conversation=obj).timestamp
    except LastViewed.DoesNotExist:
      last_viewed_timestamp = None

    try:
      last_sent_msg = Message.objects.filter(user=user, conversation=obj).latest('created_at')
      last_sent_msg_timestamp = last_sent_msg.created_at
    except Message.DoesNotExist:
      last_sent_msg_timestamp = None

    if last_sent_msg_timestamp and last_viewed_timestamp:
      if last_viewed_timestamp > last_sent_msg_timestamp:
        since_timestamp = last_viewed_timestamp
      else:
        since_timestamp = last_sent_msg_timestamp
    else:
      since_timestamp = last_sent_msg_timestamp or last_viewed_timestamp

    if since_timestamp:
      unread_count = Message.objects.filter(conversation=obj, created_at__gt=since_timestamp).count()
    else:
      unread_count = Message.objects.filter(conversation=obj).count()
      
    return unread_count

  @swagger_serializer_method(serializer_or_field=UserSnippetSerializer)
  def get_other_user(self, obj):
    user = self.context['request'].user
    participants = obj.participants
    other_user = next(u for u in participants.all() if u.id != user.id)

    return UserSnippetSerializer(other_user).data

  @swagger_serializer_method(serializer_or_field=MessageSerializer)
  def get_last_message(self, obj):
    last_message = None

    try:
      last_message = Message.objects.filter(conversation=obj).latest('created_at')
      last_message = MessageSerializer(last_message).data
    except:
      pass

    return last_message
