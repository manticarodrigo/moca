from functools import reduce 

from django.db.models import Q
from django.forms.models import model_to_dict
from rest_framework import generics, permissions, status
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from moca.api.appointment.errors import AppointmentNotFound, ReviewNotFound
from moca.api.appointment.serializers import (AppointmentCreateUpdateSerializer,
                                              AppointmentSerializer)
from moca.models.appointment import Appointment, AppointmentRequest, Review


class AppointmentListView(generics.ListAPIView):
  permission_classes = [IsAuthenticated]
  serializer_class = AppointmentSerializer

  def get_queryset(self):
    query_params = self.request.query_params
    user = self.request.user
    user_profile_model = user.get_profile_model()
    user_profile_type = user.get_profile_type()
    user_profile = user_profile_model.objects.get(user=user)

    filter_dict = {user_profile_type: user_profile}
    queries = [Q(**filter_dict)]

    start = query_params.get("start")
    if start:
      queries.append(Q(start_time__gte=start))
    
    end = query_params.get("end")
    if end:
      queries.append(Q(end_time__lte=end))

    query = reduce(lambda x, y: x & y, queries)
    return Appointment.objects.filter(query)


class AppointmentAPIDetailView(generics.RetrieveUpdateDestroyAPIView):
  lookup_url_kwarg = 'appointment_id'
  queryset = Appointment.objects.all()

  def get_serializer_class(self):
    if self.request.method == 'GET':
      return AppointmentSerializer
    else:
      return AppointmentCreateUpdateSerializer


class AppointmentRequestView(APIView):
  permission_classes = [permissions.IsAuthenticated]

  def post(self, request, appointment_request_id, request_status):
    try:
      appointment_request = AppointmentRequest.objects.get(pk=appointment_request_id)
    except AppointmentRequest.DoesNotExist:
      raise APIException('Invalid appointment request')

    current_status = appointment_request.status

    if current_status != 'pending':
      raise APIException('Appointment request already handled')

    if request_status == 'accept':
      if self.request.user.id != appointment_request.patient_id:
        raise APIException('Only patient can accept')

      appointment_request.status = 'accepted'
      appointment_to_create = model_to_dict(appointment_request)

      serializer = AppointmentCreateUpdateSerializer(data=appointment_to_create)

      if serializer.is_valid():
        created_appointment = serializer.save()
        serialized_created_appointment = AppointmentSerializer(created_appointment,
                                                               context={
                                                                 'request': request
                                                               }).data
        appointment_request.save()
        return Response(serialized_created_appointment, status.HTTP_200_OK)

      else:
        raise APIException('Appointment request handler issue')

    elif request_status == 'cancel':
      if self.request.user.id != appointment_request.therapist_id:
        raise APIException('Only therapist can cancel')
      appointment_request.status = 'cancelled'
      appointment_request.save()
      return Response("Cancelled", status=status.HTTP_200_OK)


    elif request_status == 'reject':
      appointment_request.status = 'rejected'
      appointment_request.save()
      return Response("Rejected", status=status.HTTP_200_OK)

    else:
      raise APIException('Incorrect request status')
