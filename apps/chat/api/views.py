from rest_framework.views import APIView
from django.core import serializers
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from ..models import Conversation, Participant, Message
from .serializers import MessageSerializer, UserSerializer
from .permissions import IsParticipant

class ConversationView(APIView, PageNumberPagination):
  permission_classes = [IsParticipant]

  def get(self, request, id):
    participants = [
      UserSerializer(User.objects.get(id=participant.id)).data
      for participant in Participant.objects.filter(conversation__id=id)
    ]

    self.check_object_permissions(request, participants)

    queryset = Message.objects.filter(conversation__id=id).order_by('-created_at')
    page = self.paginate_queryset(queryset, request, view=self)
    serializer = MessageSerializer(page, many=True)

    previous_link = self.get_previous_link()

    data = {
      "next": self.get_next_link(),
      "previous": previous_link,
      "count": self.page.paginator.count,
      "messages": serializer.data
    }

    if (previous_link is None):
      data["users"] = participants

    return Response(data=data)
  
  def post(self, request, id):
    participants = [
      UserSerializer(User.objects.get(id=participant.id)).data
      for participant in Participant.objects.filter(conversation__id=id)
    ]

    self.check_object_permissions(request, participants)

    conversation = Conversation.objects.get(id=id)
    message = Message(user=request.user, conversation=conversation, text=request.data['text'])
    message.save()

    serializer = MessageSerializer(message)

    return Response(serializer.data)

class ConversationListView(APIView, PageNumberPagination):

  def get(self, request):
    queryset = Participant.objects.filter(user__id=request.user.id)
    
    data = []

    for participation in queryset:
      other_participants = [
        UserSerializer(User.objects.get(id=participant.id)).data
        for participant in Participant.objects.filter(
          conversation__id=participation.conversation.id
        )
        if participant.user.id != request.user.id
      ]

      latest_message = MessageSerializer(
        Message
          .objects
          .filter(conversation__id=participation.conversation.id)
          .latest('created_at')
      ).data

      data.append({"other_participants": other_participants, "latest_message": latest_message})

    return Response(data)

  def post(self, request):
    return Response("POST")

