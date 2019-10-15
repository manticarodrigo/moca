import json


from django.db.models import F
from rest_framework import permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from moca.models.user import Patient, Therapist
from moca.models.user.user import AwayDays
from moca.models.prices import Price

from .serializers import (PatientSerializer, PatientCreateSerializer,
                          TherapistSerializer, TherapistCreateSerializer, PriceSerializer,
                          LeaveSerializer, LeaveResponseSerializer)

from .permissions import IsSelf


class PatientCreateView(generics.CreateAPIView):
  """
  POST {{ENV}}/api/user/patient
  """
  serializer_class = PatientCreateSerializer

class PatientDetailView(generics.RetrieveUpdateAPIView):
  """
  GET, PATCH {{ENV}}/api/user/patient/{id}
  """
  serializer_class = PatientSerializer
  queryset = Patient.objects
  permission_classes = [IsSelf]


class TherapistCreateView(generics.CreateAPIView):
  """
  POST {{ENV}}/api/user/therapist/
  """
  serializer_class = TherapistCreateSerializer

class TherapistDetailView(generics.RetrieveUpdateAPIView):
  """
  GET, PATCH {{ENV}}/api/user/therapist/{id}
  """
  serializer_class = TherapistSerializer
  queryset = Therapist.objects
  permission_classes = [IsSelf]


class TherapistSearchView(generics.ListAPIView):
  """
  GET {{ENV}}/api/user/therapist/search/
  """
  serializer_class = TherapistSerializer
  queryset = Therapist.objects.all()
  permission_classes = [permissions.IsAuthenticated]

  def filter_queryset(self, queryset):
    therapists = queryset
    criteria = self.request.query_params
    user = self.request.user
    user_location = None

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


    if user_location:
      METERS_PER_MILE = 1609.34

      therapists = therapists.filter(primary_location__distance_lt=(user_location,
                                                                    F('operation_radius') *
                                                                    METERS_PER_MILE))

    return therapists

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
