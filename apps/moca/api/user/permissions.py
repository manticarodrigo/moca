from rest_framework.permissions import BasePermission, IsAuthenticated


class IsSelf(IsAuthenticated):
  message = f"Current user is not allowed to edit target user"

  def has_object_permission(self, request, view, user):
    return request.user.id == user.user.id
