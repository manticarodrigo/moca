from django.contrib.auth.models import User
from rest_framework import serializers

from moca.models import Conversation, Message, TextMessage, ImageMessage
# from moca.models.chat import MediaMessage
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
  text = TextMessageSerializer()
  image = ImageMessageSerializer()
  class Meta:
    model = Message
    fields = ['type', 'created_at', 'text', 'image']


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
