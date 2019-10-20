from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.response import Response
from moca.api.appointment.serializers import AppointmentSerializer, AppointmentCreateUpdateSerializer
from moca.api.appointment.errors import AppointmentNotFound, ReviewNotFound
from moca.models.appointment import Appointment, Review


class AppointmentListCreateView(generics.ListCreateAPIView):
  permission_classes = [IsAuthenticated]

  def get_serializer_class(self):
    if self.request.method == 'POST':
      return AppointmentCreateUpdateSerializer
    else:
      return AppointmentSerializer

  def get_queryset(self):
    user = self.request.user
    user_profile_model = user.get_profile_model()
    user_profile_type = user.get_profile_type()
    user_profile = user_profile_model.objects.get(user=user)
    filter_dict = {user_profile_type: user_profile}
    return Appointment.objects.filter(**filter_dict)


class AppointmentAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
  lookup_url_kwarg = 'appointment_id'
  queryset = Appointment.objects.all()

  def get_serializer_class(self):
    if self.request.method == 'GET':
      return AppointmentSerializer
    else:
      return AppointmentCreateUpdateSerializer
