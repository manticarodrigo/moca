from rest_framework.permissions import BasePermission, IsAuthenticated

SAFE_METHODS = ['GET', 'HEAD', 'OPTIONS']



class IsUserSelf(IsAuthenticated):
  message = f"You are not allowed to edit the target user."

  def has_object_permission(self, request, view, user):
    return request.user.id == user.id


class IsObjectUserSelfOrReadonly(IsAuthenticated):
  message = f"You are not allowed to edit the target user."

  def has_object_permission(self, request, view, obj):
    if (request.method in SAFE_METHODS):
      return True
    return request.user.id == obj.user.id


class IsObjectPatientSelfOrReadonly(IsAuthenticated):
  message = f"Only the patient is allow to make edits."

  def has_object_permission(self, request, view, obj):
    if (request.method in SAFE_METHODS):
      return True
    return request.user.id == obj.patient.user.id


class IsObjectTherapistSelfOrReadonly(IsAuthenticated):
  message = f"Only the therapist is allow to make edits."

  def has_object_permission(self, request, view, obj):
    if (request.method in SAFE_METHODS):
      return True
    return request.user.id == obj.therapist.user.id
