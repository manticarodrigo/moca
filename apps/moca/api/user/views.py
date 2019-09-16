from django.forms.models import model_to_dict
from django.http import Http404
from knox.models import AuthToken
from rest_framework import status
from rest_framework.exceptions import MethodNotAllowed, AuthenticationFailed
import json
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import (APIView)
from moca.models.address import Address
from fcm_django.models import FCMDevice, Device
from django.shortcuts import get_object_or_404

from moca.models import User
from moca.models.user import Patient
from .serializers import AddressSerializer, FCMDeviceSerializer, PatientSerializer, TherapistSerializer, UserSerializer, \
  UserRequestSerializer
from .serializers import PatientSerializer


# {{ENV}}/api/user/patient
class PatientAPIView(APIView):
  def post(self, request, format=None):
    request_serializer = UserRequestSerializer(data=request.data)
    request_serializer.is_valid(raise_exception=True)
    user = request_serializer.save()
    user = User.objects.get(id=user.id)
    response = UserSerializer(user)
    return Response( response.data,status.HTTP_201_CREATED )


# {{ENV}}/api/user/patient/id
class PatientAPIDetail(APIView):

  # todo prevent post request coming this view
  def get(self, request, patient_id, format=None):
    patient = Patient.objects.get_patient(patient_id)
    serializer = PatientSerializer(patient)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def put(self, request, user_id, format=None):
    url_user = self.get_object(user_id)
    request_body = request.data
    self.is_belong_to_auth_user(request, url_user)

    return Response({"user": PatientSerializer().data})

  def set_user_id_if_nonexists(self, addr, request):
    try:
      addr["user"] = request.user.id
    except AttributeError:
      addr["user"] = request.user.id

  def validate_addresses(self, addresses, user_id):
    for address in addresses:
      if self.is_update(a=address):
        existing_address = get_object_or_404(Address, pk=address['id'])
        if existing_address is None:
          return Response(f'Address doesnt exists with id {address[id]}',
                          status.HTTP_400_BAD_REQUEST)

  def is_belong_to_auth_user(self, request, url_user):
    if url_user is None:
      raise MethodNotAllowed("")
    elif url_user != request.user:
      raise AuthenticationFailed('UserId in URL doesnt match with the id of authenticated user')

  def is_update(self, a):
    try:
      address_id = a['id']
      return True
    except KeyError:
      return False

  def delete(self, request, pk, format=None):
    snippet = self.get_object(pk)
    snippet.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

  @staticmethod
  def get_object(pk):
    try:
      return User.objects.get(pk=pk)
    except User.DoesNotExist:
      raise Http404


class TherapistAPIView(APIView):
  def post(self, request, format=None):
    therapist_serializer = TherapistSerializer(data=request.data)
    # TODO decide which one is correct by testing
    therapist_serializer.is_valid(raise_exception=True)
    therapist = therapist_serializer.save()
    return Response(therapist_serializer.data, status.HTTP_201_CREATED)


class TherapistAPIDetailView(APIView):
  def get(self, request, patient_id, format=None):
    pass

  def get(self, request, patient_id, format=None):
    pass


class UserDeviceView(APIView):
  @staticmethod
  def get(request):
    device_serializer = FCMDeviceSerializer(data=FCMDevice.objects.all(), many=True)
    if device_serializer.is_valid():
      return Response(device_serializer.errors, status.HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=device_serializer.data, status=status.HTTP_200_OK)

  def post(self, request, format=None):
    device_serializer = FCMDeviceSerializer(data=request.data)
    if not device_serializer.is_valid():
      return Response(device_serializer.errors, status.HTTP_400_BAD_REQUEST)
    device_serializer.save()
    return Response(device_serializer.data, status=status.HTTP_201_CREATED)

  def delete(self, request):
    Address.objects.all().delete()
    FCMDevice.objects.all().delete()
    User.objects.all().delete()
    return Response(status=status.HTTP_202_ACCEPTED)
