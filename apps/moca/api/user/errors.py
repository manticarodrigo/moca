from rest_framework import status
from rest_framework.exceptions import APIException


class EditsNotAllowed(APIException):
  status_code = status.HTTP_403_FORBIDDEN
  def __init__(self, current_user_id, target_user_id):
    self.detail = f"User {current_user_id} is not allowed to edit {target_user_id}"
