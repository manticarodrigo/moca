from rest_framework.permissions import IsAuthenticated

class HasCancellationRights(IsAuthenticated):
  message = 'Unauthorized access'

  def has_object_permission(self, request, view, appointment):
    user_id = request.user.id 
    patient_id = appointment.patient_id 
    therapist_id = appointment.therapist_id
    return user_id in [therapist_id, patient_id] and not appointment.is_cancelled