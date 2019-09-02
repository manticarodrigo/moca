from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from moca.models import (AttachmentMessage, Conversation, Message,
                         MessageTypes, RequestMessage, ResponseMessage,
                         TextMessage)

from .errors import (ConversationNotFound, InvalidMessageType, RequestNotFound,
                     ResponseConflict, SelfChatNotAllowed, UserNotFound)
from .serializers import (AttachmentSerializer, ConversationSerializer,
                          MessageSerializer, RequestSerializer,
                          ResponseSerializer, TextMessageSerializer,
                          UserSerializer)

User = get_user_model()


class ChatAPI(GenericAPIView):
  permission_classes = [permissions.IsAuthenticated]

  # TODO use builtin serializer

  @transaction.atomic
  def post(self, request):
    """
    Creates a new chat
    """
    # TODO get the participants from a query param, body should be empty
    participant_ids = set(request.data['participants'])
    participant_ids.add(request.user.id)
    conversation = Conversation.objects.create()

    if len(participant_ids) < 2:
      raise SelfChatNotAllowed()

    for participant_id in participant_ids:
      try:
        new_participant = User.objects.get(id=participant_id)
        conversation.participants.add(new_participant)
      except User.DoesNotExist:
        raise UserNotFound(participant_id)

    conversation.save()
    return Response(ConversationSerializer(conversation).data)

  def get(self, request):
    """
    Returns a list of all conversations for the current user
    """
    conversations = Conversation.objects.filter(participants=request.user)

    return Response(ConversationSerializer(conversations, many=True).data,
                    status=status.HTTP_201_CREATED)


# TODO check ListCreateAPIView usage
class MessagesAPI(GenericAPIView):
  permission_classes = [permissions.IsAuthenticated]

  @staticmethod
  def handle_request_message(sender, conversation, message):
    new_message = RequestMessage.objects.create(user=sender,
                                                conversation=conversation,
                                                options=message['options'])
    new_message.save()
    return RequestSerializer(new_message).data

  @staticmethod
  @transaction.atomic
  def handle_response_message(sender, conversation, message):
    # TODO this will change after RequestMessage changes.
    # TODO use a serializer here
    reply_to = message['reply_to']
    selection = message['selection']

    request = RequestMessage.objects.filter(id=reply_to, conversation=conversation).first()

    print(request.responsemessage_set.count())

    if not request:
      raise RequestNotFound(reply_to, conversation.id)

    if request.responsemessage_set.count() > 0:
      raise ResponseConflict(request_id=request.id,
                             existing_response_id=request.responsemessage_set.first().id)

    answer = request.options[selection]

    response_message = ResponseMessage.objects.create(user=sender,
                                                      conversation=conversation,
                                                      reply_to=request,
                                                      selection=selection)

    if answer == 'ACCEPT':
      # Create the appointment here based on the request being an appointment and the date
      # of the request
      pass

    response_message.save()

    return ResponseSerializer(response_message).data

  @staticmethod
  def handle_attachment_message(sender, conversation, message):
    return AttachmentSerializer(message).data

  @staticmethod
  def handle_text_message(sender, conversation, message):
    new_message = TextMessage.objects.create(user=sender,
                                             conversation=conversation,
                                             text=message['text'])
    new_message.save()
    return TextMessageSerializer(new_message).data

  def post(self, request, convid):
    """
    Sends a new message
    """
    user = request.user
    conversation = Conversation.objects.filter(id=convid, participants=user).first()

    if not conversation:
      raise ConversationNotFound(convid)

    created = None
    message_data = {"sender": user, "conversation": conversation, "message": request.data['data']}
    message_type = request.data['type']

    if message_type == MessageTypes.REQUEST:
      created = MessagesAPI.handle_request_message(**message_data)
    elif message_type == MessageTypes.RESPONSE:
      created = MessagesAPI.handle_response_message(**message_data)
    elif message_type == MessageTypes.TEXT:
      created = MessagesAPI.handle_text_message(**message_data)
    elif message_type == MessageTypes.ATTACHMENT:
      created = MessagesAPI.handle_attachment_message(**message_data)
    else:
      raise InvalidMessageType(message_type)

    # TODO(ukaya) Handle firebase here

    # TODO check for a quicker way of created and/or forbidden
    return Response(created, status=status.HTTP_201_CREATED)

  def get(self, request, convid):
    """
    Gets all messages in a conversation
    """
    # TODO fix this to use generic foreign keys to figure out how to serialize each message based
    # on its type
    messages = Message.objects.filter(conversation__id=convid)
    return Response({"messages": MessageSerializer(messages, many=True).data})
