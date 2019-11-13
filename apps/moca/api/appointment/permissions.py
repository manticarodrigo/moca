from rest_framework.permissions import IsAuthenticated


class IsParticipant(IsAuthenticated):
  message = 'Unauthorized access'

  def has_object_permission(self, request, view, appointment):
    user_id = request.user.id
    patient_id = appointment.patient_id
    therapist_id = appointment.therapist_id
    return user_id in [therapist_id, patient_id]


class CanCancel(IsParticipant):
  message = 'Invalid action'

  def has_object_permission(self, request, view, appointment):
    return appointment.status == 'not-started'


class CanStart(IsParticipant):
  message = 'Invalid action'

  def has_object_permission(self, request, view, appointment):
    return appointment.status == 'not-started'


class CanEnd(IsParticipant):
  message = 'Invalid action'

  def has_object_permission(self, request, view, appointment):
    return appointment.status == 'in-progress'
