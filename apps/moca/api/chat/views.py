from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import permissions, status
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from moca.models import Conversation, Message, Participant

from .permissions import IsParticipant
from .serializers import MessageSerializer, UserSerializer, ConversationSerializer

User = get_user_model()


class ConversationView(APIView, PageNumberPagination):
  # permission_classes = [IsParticipant]

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

    if previous_link is None:
      data["participants"] = participants

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
          conversation__id=participation.conversation.id) if participant.user.id != request.user.id
      ]

      latest_message = MessageSerializer(
        Message.objects.filter(
          conversation__id=participation.conversation.id).latest('created_at')).data

      data.append({
        "id": participation.conversation.id,
        "other_participants": other_participants,
        "latest_message": latest_message
      })

    return Response(data)


class ChatAPI(GenericAPIView):
  permission_classes = [permissions.IsAuthenticated]

  # TODO use builtin serializer

  def post(self, request):
    """
    Creates a new chat
    """

    # TODO get the participants from a query param, body should be empty
    participant_ids = set(request.data['participants'])
    participant_ids.add(request.user.id)

    conversation = Conversation.objects.create()

    if len(participant_ids) < 2:
      return Response(status=400, data={"error": "Can't create a chat with yourself"})

    for participant_id in participant_ids:
      new_participant = Participant.objects.create(conversation=conversation,
                                                   user=User.objects.get(id=participant_id))
      conversation.participant_set.add(new_participant)

    conversation.save()
    return Response(ConversationSerializer(conversation).data)

  def get(self, request):
    """
    Returns a list of all conversations for the current user
    """

    # TODO check if there's a more direct way
    conversation_ids = Participant.objects.filter(user=request.user).values('conversation')
    conversations = Conversation.objects.filter(id__in=conversation_ids)

    return Response(ConversationSerializer(conversations, many=True).data)


# TODO check ListCreateAPIView usage
class MessagesAPI(GenericAPIView):
  permission_classes = [permissions.IsAuthenticated]

  def post(self, request, convid):
    """
    Sends a new message
    """
    user = request.user

    conversation = Conversation.objects.get(id=convid)
    is_participant = conversation.participant_set.get_queryset().filter(user=user).count() == 1

    if not is_participant:
      return Response({"error": "User not part of this conversation"},
                      status=status.HTTP_403_FORBIDDEN)

    message = Message.objects.create(conversation=conversation,
                                     text=request.data['message'],
                                     user=user)

    message.save()

    # TODO(ukaya) Handle firebase here

    # TODO check for a quicker way of created and/or forbidden
    return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)

  def get(self, request, convid):
    """
    Gets all messages in a conversation
    """
    messages = Message.objects.filter(conversation__id=convid)
    return Response({"messages": MessageSerializer(messages, many=True).data})
