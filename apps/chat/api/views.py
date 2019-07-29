from rest_framework.views import APIView
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User, Group
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from ..models import Message, Participant
from .serializers import MessageSerializer, UserSerializer


class Conversation(APIView):
  permission_classes = (IsAuthenticated,)
  
  def get(self, request, id):
    messages_queryset = Message.objects.filter(conversation__id=id).order_by('created_at')

    participants = [
      UserSerializer(User.objects.get(id=participant.id)).data
      for participant in Participant.objects.filter(conversation__id=id)
    ]

    print(request.user, participants)
    if (request.user not in participants):
      raise PermissionDenied()
      
    messages = MessageSerializer(messages_queryset, many=True).data

    data = {"users": participants, "messages": messages}

    return Response(data=data)



class ConversationList(APIView):
  def get(self, request):
    return Response("LIST")

  def post(self, request):
    return Response("POST")


