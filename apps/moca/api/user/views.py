import json

from django.forms.models import model_to_dict
from django.http import Http404
from django.shortcuts import get_object_or_404
from fcm_django.models import Device, FCMDevice
from knox.models import AuthToken
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, MethodNotAllowed
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from moca.models import User
from moca.models.address import Address
from moca.models.user import Patient, Therapist

from .serializers import (AddressSerializer, FCMDeviceSerializer, PatientRequestSerializer,
                          PatientSerializer, TherapistRequestSerializer, TherapistSerializer,
                          UserRequestSerializer, UserSerializer)


# {{ENV}}/api/user/patient
class PatientAPIView(APIView):
  def post(self, request, format=None):
    patient_req_serializer = PatientRequestSerializer(data=request.data)
    patient_req_serializer.is_valid(raise_exception=True)
    patient = patient_req_serializer.save()
    return Response(
      {
        "user": UserSerializer(patient.user).data,
        "addresses": AddressSerializer(patient.user.addresses, many=True).data,
        "devices": FCMDeviceSerializer(patient.user.fcmdevice_set_set.data, many=True).data,
        "token": AuthToken.objects.create(patient.user)[1]
      }, status.HTTP_201_CREATED)


# {{ENV}}/api/user/patient/id
class PatientAPIDetail(APIView):

  # todo prevent post request coming this view
  def get(self, request, patient_id, format=None):
    patient = Patient.objects.get(pk=patient_id)
    serializer = UserSerializer(patient.user)
    return Response(serializer.data, status=status.HTTP_200_OK)

  def put(self, request, patient_id, format=None):
    patient = get_object_or_404(Patient, patient_id)
    existing = get_object_or_404(User, patient.user_id)
    self.is_belong_to_auth_user(request, existing)
    req_serializer = UserRequestSerializer(instance=existing, data=request.data)
    req_serializer.is_valid(raise_exception=True)
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
  valid_criteria = ['gender', 'orderby']

  def post(self, request, format=None):
    therapist_req_serializer = TherapistRequestSerializer(data=request.data)
    therapist_req_serializer.is_valid(raise_exception=True)
    therapist = therapist_req_serializer.save()

    return Response(
      {
        "user": UserSerializer(therapist.user).data,
        "therapist": TherapistSerializer(therapist).data,
        "addresses": AddressSerializer(therapist.user.addresses, many=True).data,
        "devices": FCMDeviceSerializer(therapist.user.fcmdevice_set, many=True).data,
      }, status.HTTP_201_CREATED)

  def get(self, request):
    from django.contrib.gis.db.models.functions import Distance
    from .serializers import TherapistSerializer
    criteria = request.query_params

    # TODO add location filter for out-of-area therapists

    therapists = Therapist.objects

    if 'gender' in criteria:
      therapists = therapists.filter(user__gender=criteria['gender'])

    return Response(TherapistSerializer(therapists, many=True).data)


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
