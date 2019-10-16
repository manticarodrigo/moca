from rest_framework import status
from rest_framework.exceptions import APIException

class DuplicateEmail(APIException):
  status_code = status.HTTP_409_CONFLICT

  def __init__(self, given_email):
    self.detail = f'Email \'{given_email}\' has already been registered.'
