from rest_framework.permissions import BasePermission, IsAuthenticated


class IsParticipant(IsAuthenticated):
  message = 'You are not a participant in this conversation.'

  def has_object_permission(self, request, view, participants):
    return request.user.id in [participant['id'] for participant in participants]
