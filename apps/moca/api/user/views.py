from django.http import Http404
from django.shortcuts import get_object_or_404
from knox.models import AuthToken
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, MethodNotAllowed
from rest_framework.response import Response
from rest_framework.views import APIView

from moca.models import User
from moca.models.user import Patient, Therapist
from .serializers import (AddressSerializer, FCMDeviceSerializer, PatientRequestSerializer,
                          TherapistRequestSerializer, TherapistSerializer, UserRequestSerializer,
                          UserSerializer)


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


class TherapistAPIView(APIView):
  valid_criteria = ['gender', 'orderby']

  def post(self, request, format=None):
    therapist_req_serializer = TherapistRequestSerializer(data=request.data)
    therapist_req_serializer.is_valid(raise_exception=True)
    therapist = therapist_req_serializer.save()

    return Response(
      {
        **TherapistSerializer(therapist).data, "token": AuthToken.objects.create(therapist.user)[1]
      }, status.HTTP_201_CREATED)

  def get(self, request):
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

  def put(self, request, patient_id, format=None):
    pass
