from rest_framework.permissions import BasePermission, IsAuthenticated

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']


class IsSelfOrReadonly(IsAuthenticated):
  """
  The request is authenticated as the target user, or is a read-only request.
  """
  message = f"Current user is not allowed to edit target user"

  # TODO this doesn't make sense
  def has_object_permission(self, request, view, user):
    if (request.method in SAFE_METHODS):
      return True
    return request.user.id == user.user.id
