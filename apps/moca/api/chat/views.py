# from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework import generics 
from rest_framework.exceptions import APIException
# from rest_framework.response import Response

# from moca.api.appointment.serializers import AppointmentSerializer, AppointmentDeserializer
from moca.models import Conversation, Message
# from moca.models.appointment import Appointment
# from moca.models.chat import MediaMessage, AppointmentMessage

# from .errors import (ConversationNotFound, InvalidMessageType, RequestNotFound, ResponseConflict,
#                      SelfChatNotAllowed, UserNotFound)
# from .serializers import (ConversationSerializer, MessageSerializer, MediaMessageSerializer,
#                           AppointmentMessageSerializer)

from .serializers import ConversationSerializer, MessageSerializer
# User = get_user_model()


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

    if (target_user_id == user_id):
      raise APIException('Sender and Recepient are the same.')
    
    conversation = Conversation.objects \
                    .filter(participants__id=user_id) \
                    .filter(participants__id=target_user_id)
    messages = Message.objects.filter(conversation__in=conversation).order_by('created_at')
    return messages



#   # TODO use builtin serializer

#   @transaction.atomic
#   def post(self, request):
#     """
#     Creates a new chat
#     """
#     # TODO get the participants from a query param, body should be empty
#     participant_ids = set(request.data['participants'])
#     participant_ids.add(request.user.id)
#     conversation = Conversation.objects.create()

#     if len(participant_ids) < 2:
#       raise SelfChatNotAllowed()

#     for participant_id in participant_ids:
#       try:
#         new_participant = User.objects.get(id=participant_id)
#         conversation.participants.add(new_participant)
#       except User.DoesNotExist:
#         raise UserNotFound(participant_id)

#     conversation.save()
#     return Response(ConversationSerializer(conversation).data, status.HTTP_201_CREATED)

#   def get(self, request):
#     """
#     Returns a list of all conversations for the current user
#     """
#     conversations = Conversation.objects.filter(participants=request.user)

#     return Response(ConversationSerializer(conversations, many=True).data,
#                     status=status.HTTP_201_CREATED)


# # TODO check ListCreateAPIView usage
# class MessagesAPI(GenericAPIView):
#   permission_classes = [permissions.IsAuthenticated]

#   @staticmethod
#   @transaction.atomic
#   def handle_request_message(sender, conversation, message):
#     appointment = AppointmentDeserializer(data=message)
#     appointment.is_valid(raise_exception=True)
#     appointment = appointment.save()
#     new_message = AppointmentMessage.objects.create(user=sender,
#                                                     conversation=conversation,
#                                                     appointment=appointment)
#     new_message.save()
#     return AppointmentMessageSerializer(new_message).data

#   @staticmethod
#   @transaction.atomic
#   def handle_response_message(sender, conversation, message):
#     # TODO use a serializer here
#     reply_to = message['request_id']
#     response = message['response']

#     request = AppointmentMessage.objects.filter(id=reply_to, conversation=conversation).first()

#     if not request:
#       raise RequestNotFound(reply_to, conversation.id)

#     if not request.response is None:
#       raise ResponseConflict(request_id=request.id, existing_response=request.response)

#     if response == 'REJECTED':
#       appointment_id = request.appointment_id
#       appointment = Appointment.objects.get(pk=appointment_id)
#       appointment.is_cancelled = True
#       appointment.save()

#     request.response = response
#     request.save()
#     request = AppointmentMessage.objects.filter(id=reply_to, conversation=conversation).first()

#     return AppointmentMessageSerializer(request).data

#   @staticmethod
#   def handle_media_message(sender, conversation, message):
#     new_message = MediaMessage.objects.create(user=sender,
#                                               conversation=conversation,
#                                               text=message['text'],
#                                               file=message['file'],
#                                               mediaType=message['mediatype'])
#     new_message.save()
#     return MediaMessageSerializer(new_message).data

#   @staticmethod
#   def handle_message(message_type, message_data):
#     created = None

#     if message_type == MessageTypes.REQUEST:
#       created = MessagesAPI.handle_request_message(**message_data)
#     elif message_type == MessageTypes.RESPONSE:
#       created = MessagesAPI.handle_response_message(**message_data)
#     elif message_type == MessageTypes.MEDIA:
#       created = MessagesAPI.handle_media_message(**message_data)
#     else:
#       raise InvalidMessageType(message_type)

#     return created

#   def post(self, request, convid):
#     """
#     Sends a new message
#     """
#     user = request.user
#     conversation = Conversation.objects.filter(id=convid, participants=user).first()

#     if not conversation:
#       raise ConversationNotFound(convid)

#     message_data = {"sender": user, "conversation": conversation, "message": request.data['data']}
#     message_type = request.data['type']

#     created = MessagesAPI.handle_message(message_type, message_data)

#     # TODO(rodrigo) Push Notification service should be called here

#     return Response(created, status=status.HTTP_201_CREATED)

#   def get(self, request, convid):
#     """
#     Gets all messages in a conversation
#     """
#     # TODO fix this to use generic foreign keys to figure out how to serialize each message based
#     # on its type

#     media_messages = MediaMessage.objects.filter(conversation__id=convid)
#     appointment_messages = AppointmentMessage.objects.filter(conversation__id=convid)

#     media_messages = MediaMessageSerializer(media_messages, many=True).data
#     appointment_messages = AppointmentMessageSerializer(appointment_messages, many=True).data

#     return Response({"messages": media_messages + appointment_messages})
