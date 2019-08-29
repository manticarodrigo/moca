from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework import permissions, status
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

  def post(self, request):
    """
    Creates a new chat
    """
    participant_ids = set(request.data['participants'])
    participant_ids.add(User.objects.get(email=request.user).id)

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
    user = User.objects.get(email=request.user)
    conversation_ids = Participant.objects.filter(user=user).values('conversation')
    conversations = map(lambda conv: ConversationSerializer(conv).data,
                        Conversation.objects.filter(id__in=conversation_ids))

    return Response(conversations)


class MessagesAPI(GenericAPIView):
  permission_classes = [permissions.IsAuthenticated]

  def post(self, request, convid):
    """
    Sends a new message
    """

    user = User.objects.get(email=request.user)

    conversation = Conversation.objects.get(id=convid)
    participants = list(conversation.participant_set.values('user'))

    if {'user': user.id} not in participants:
      return Response({"error": "User not part of this conversation"},
                      status=status.HTTP_403_FORBIDDEN)

    message = Message.objects.create(conversation=conversation,
                                     text=request.data['message'],
                                     user=user)

    message.save()

    # TODO(ukaya) Handle firebase here

    return Response(MessageSerializer(message).data, status=status.HTTP_201_CREATED)

  def get(self, request, convid):
    """
    Gets all messages in a conversation
    """
    messages = map(lambda message: MessageSerializer(message).data,
                   Message.objects.filter(conversation__id=convid))
    return Response({"messages": messages})
