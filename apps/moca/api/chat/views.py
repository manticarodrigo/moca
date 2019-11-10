from rest_framework import permissions
from rest_framework import generics
from rest_framework.exceptions import APIException
from django.utils import timezone

from moca.models import Conversation, Message, LastViewed
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
    user = self.request.user
    user_id = user.id
    target_user_id = self.kwargs['user_id']

    if target_user_id == user_id:
      raise APIException('Sender and Recepient are the same.')

    conversation = Conversation.objects \
                    .filter(participants__id=user_id) \
                    .filter(participants__id=target_user_id).first()

    limit_param = self.request.query_params.get("limit")
    parsed_limit = limit_param and int(limit_param)
    messages = Message.objects.filter(
      conversation=conversation).order_by('-created_at')[:parsed_limit][::-1]

    if conversation:
      now_timestamp = timezone.now()
      LastViewed.objects.update_or_create(conversation=conversation,
                                          user=user,
                                          defaults={"timestamp": now_timestamp})
    return messages
