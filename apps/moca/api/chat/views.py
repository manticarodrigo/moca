from rest_framework import permissions
from rest_framework import generics
from rest_framework.exceptions import APIException

from moca.models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class ConversationListView(generics.ListAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = ConversationSerializer

  def get_queryset(self):
    user_id = self.request.user.id
    return Conversation.objects.filter(participants__id=user_id)


class MessageListCreateView(generics.ListCreateAPIView):
  permission_classes = [permissions.IsAuthenticated]
  serializer_class = MessageSerializer

  def get_queryset(self):
    user_id = self.request.user.id
    target_user_id = self.kwargs['user_id']

    if target_user_id == user_id:
      raise APIException('Sender and Recepient are the same.')

    conversation = Conversation.objects \
                    .filter(participants__id=user_id) \
                    .filter(participants__id=target_user_id)
    messages = Message.objects.filter(conversation__in=conversation).order_by('created_at')
    return messages
