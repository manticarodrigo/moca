import json


from rest_framework import generics

from django.db.models import F
from django.http import Http404
from django.shortcuts import get_object_or_404
from knox.models import AuthToken
from rest_framework import permissions, status, generics
from rest_framework.exceptions import AuthenticationFailed, MethodNotAllowed
from rest_framework.response import Response
from rest_framework.views import APIView

from moca.models import User, Price
from moca.models.user import Patient, Therapist
from moca.models.user.user import AwayDays

from .errors import EditsNotAllowed
from .serializers import (AddressSerializer, PatientSerializer, PatientCreateSerializer,
                          TherapistSerializer, TherapistCreateSerializer,
                          LeaveSerializer, LeaveResponseSerializer)

# POST {{ENV}}/api/user/address
class AddressCreateView(generics.CreateAPIView):
  serializer_class = AddressSerializer

# POST {{ENV}}/api/user/patient
class PatientCreateView(generics.CreateAPIView):
  serializer_class = PatientCreateSerializer

# GET, UPDATE {{ENV}}/api/user/patient/{id}
class PatientDetailView(generics.RetrieveUpdateAPIView):
  serializer_class = PatientSerializer
  queryset = Patient.objects

# POST {{ENV}}/api/user/therapist
class TherapistCreateView(generics.CreateAPIView):
  serializer_class = TherapistCreateSerializer

# GET, UPDATE {{ENV}}/api/user/therapist/{id}
class TherapistDetailView(generics.RetrieveUpdateAPIView):
  serializer_class = TherapistSerializer
  queryset = Therapist.objects

# GET {{ENV}}/api/user/therapist
class TherapistSearchView(generics.ListAPIView):
  serializer_class = TherapistSerializer
  queryset = Therapist.objects
  permission_classes = [permissions.IsAuthenticated]

  def filter_queryset(self, queryset):
    criteria = self.request.query_params
    user = self.request.user

    if user.addresses.all().exists():
      user_location = user.addresses.get(primary=True).location

if 'gender' in criteria:
      gender = criteria['gender']
      therapists = therapists.filter(user__gender=gender)

    if 'ailments' in criteria:
      ailments = json.loads(criteria['ailments'])
      therapists = therapists.filter(preferred_ailments__contains=ailments)

    if 'max_price' in criteria:
      max_price = int(criteria['max_price'])
      therapists_in_price_range = Price.objects.filter(price__lte=max_price).values('therapist')
      therapists = therapists.filter(user_id__in=therapists_in_price_range)

    METERS_PER_MILE = 1609.34

    therapists = therapists.filter(primary_location__distance_lt=(user_location,
                                                                  F('operation_radius') *
                                                                  METERS_PER_MILE))
      return therapists
    return []

class TherapistLeaveView(APIView):
  def post(self, request, format=None):
    awaydays = LeaveSerializer(data=request.data)
    awaydays.is_valid(raise_exception=True)
    awaydays = awaydays.save()
    awaydays = AwayDays.objects.get(pk=awaydays.id)
    return Response(LeaveResponseSerializer(awaydays).data, status.HTTP_201_CREATED)


class TherapistLeaveDetailView(APIView):
  def delete(self, request, leave_id, format=None):
    AwayDays.objects.get(id=leave_id).delete()
    return Response('Leave succesfully deleted', status.HTTP_200_OK)

class TherapistPricing(generics.CreateAPIView):
  serializer_class = PriceSerializer
