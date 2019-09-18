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

from moca.models.user import Therapist
from .serializers import AddressSerializer, FCMDeviceSerializer, PatientSerializer, TherapistSerializer, UserSerializer, \
  UserRequestSerializer, PatientRequestSerializer, TherapistRequestSerializer
from .serializers import PatientSerializer


# {{ENV}}/api/user/patient
class PatientAPIView(APIView):
  def post(self, request, format=None):
    patient_req_serializer = PatientRequestSerializer(data=request.data)
    patient_req_serializer.is_valid(raise_exception=True)
    print(f'post1')
    (user, addresses, devices, patient) = patient_req_serializer.save()
    print(f'post2 addresses {addresses}')
    print(f'post3 devices {devices}')
    user = User.objects.filter(patient=patient)[0]
    return Response(
      {
        "user": UserSerializer(user).data,
        # todo deserializer only accepts one object.
        #  find a way to deserialize array for device and addresses
        "addresses": AddressSerializer(addresses[0]).data,
        "devices": FCMDeviceSerializer(devices[0]).data,
        "token": AuthToken.objects.create(user)[1]
      },
      status.HTTP_201_CREATED)


# {{ENV}}/api/user/patient/id
class PatientAPIDetail(APIView):

  # todo prevent post request coming this view
  def get(self, request, patient_id, format=None):
    print('get0')
    patient = Patient.objects.get(pk=patient_id)
    serializer = UserSerializer(patient.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def put(self, request, patient_id, format=None):
    print('api0')
    patient = get_object_or_404(Patient, patient_id)
    print('api1')
    existing = get_object_or_404(User, patient.user_id)
    print('api2')
    self.is_belong_to_auth_user(request, existing)
    print('api3')
    req_serializer = UserRequestSerializer(instance=existing, data=request.data)
    print('api4')
    req_serializer.is_valid(raise_exception=True)
    print('api5')
    user, addresses, devices = req_serializer.save()

    return Response({
      "user": UserSerializer(user).data,
      # todo deserializer only accepts one object.
      #  find a way to deserialize array for device and addresses
      "addresses": AddressSerializer(addresses[0]).data,
      "devices": FCMDeviceSerializer(devices[0]).data
    })

  def set_user_id_if_nonexists(self, addr, request):
    try:
      addr["user"] = request.user.id
    except AttributeError:
      addr["user"] = request.user.id

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
    print('therapost0')
    therapist_req_serializer = TherapistRequestSerializer(data=request.data)
    print('therapost1')
    therapist_req_serializer.is_valid(raise_exception=True)
    print('therapost2')
    user, addresses, devices, therapist = therapist_req_serializer.save()
    print(f'therapost3 {therapist}')

    return Response(
      {
        "user": UserSerializer(user).data,
        "therapist": TherapistSerializer(therapist).data,
        # todo deserializer only accepts one object.
        #  find a way to deserialize array for device and addresses
        "addresses": AddressSerializer(addresses[0]).data,
        "devices": FCMDeviceSerializer(devices[0]).data,
      },
      status.HTTP_201_CREATED)


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
