from rest_framework.permissions import IsAuthenticated


class IsOwner(IsAuthenticated):
  message = 'Unauthorized access'

  def has_object_permission(self, request, view, payment):
    print("PERMISSION")
    user_id = request.user.id
    return user_id == payment.user.id
