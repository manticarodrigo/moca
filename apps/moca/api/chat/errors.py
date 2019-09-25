from rest_framework import status
from rest_framework.exceptions import APIException, NotFound


class SelfChatNotAllowed(APIException):
  status_code = status.HTTP_400_BAD_REQUEST
  default_detail = "A chat with one participant is not allowed"


class UserNotFound(NotFound):
  def __init__(self, id):
    self.detail = f'User with id {id} not found'


class AppointmentNotFound(NotFound):
  def __init__(self, id):
    self.detail = f'Appointment with id {id} not found'


class ReviewNotFound(NotFound):
  def __init__(self, id):
    self.detail = f'Review with id {id} not found'


class ConversationNotFound(NotFound):
  def __init__(self, id):
    self.detail = f'Conversation with id {id} not found'


class RequestNotFound(NotFound):
  def __init__(self, id, convid):
    self.detail = f'No request with id {id} found in conversation with id {convid}'


class ResponseConflict(APIException):
  status_code = status.HTTP_409_CONFLICT

  def __init__(self, request_id, existing_response_id):
    self.detail = f'A response for request with id {request_id} is already provided in response {existing_response_id}'


class InvalidMessageType(APIException):
  status_code = status.HTTP_400_BAD_REQUEST

  def __init__(self, given_type):
    self.detail = f'Invalid message type \'{given_type}\''
