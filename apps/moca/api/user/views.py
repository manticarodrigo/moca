import json
from functools import reduce 

from django.db.models import Avg, Count, F, Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, permissions, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView

from moca.models import Address, EmailVerification, User, TherapistCertification
from moca.models.prices import Price
from moca.models.user import Patient, Therapist
from moca.models.user.user import AwayDays
from moca.services import canned_messages
from moca.services.emails import send_email

from .permissions import IsSelfOrReadonly
from .serializers import (LeaveResponseSerializer, LeaveSerializer, PatientCreateSerializer,
                          PatientSerializer, PriceSerializer, TherapistCreateSerializer,
                          TherapistSearchSerializer, TherapistSerializer, TherapistCertificationSerializer)


@api_view(['GET'])
def verify_email(request, token):
  emailVerification = get_object_or_404(EmailVerification, token=token)
  if emailVerification.status not in (EmailVerification.EXPIRED, EmailVerification.VERIFIED):
    emailVerification.status = EmailVerification.VERIFIED
    emailVerification.save()

    emailVerification.user.is_active = True
    emailVerification.user.save()

    if emailVerification.user.type == User.PATIENT_TYPE:
      send_email(emailVerification.user, **canned_messages.WELCOME_PATIENT)
    elif emailVerification.user.type == User.THERAPIST_TYPE:
      send_email(emailVerification.user, **canned_messages.WELCOME_PHYSICAL_THERAPIST)

    # TODO this should be a rendered template or a redirect(which should open the app)
    return Response("Verified")
  else:
    # TODO this should be a rendered template
    return Response("Token expired")


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
  permission_classes = [IsSelfOrReadonly]


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
  permission_classes = [IsSelfOrReadonly]


class TherapistSearchView(generics.ListAPIView):
  """
  GET {{ENV}}/api/user/therapist/search/
  """
  serializer_class = TherapistSearchSerializer
  queryset = Therapist.objects.annotate(Count('prices')).filter(prices__count__gt=0)
  permission_classes = [permissions.IsAuthenticated]

  def filter_queryset(self, queryset):
    therapists = queryset
    criteria = self.request.query_params
    user = self.request.user
    user_location = None

    try:
      user_location = Address.objects.get(user=user, primary=True).location
    except Address.DoesNotExist:
      raise APIException('No primary address found.')

    if 'gender' in criteria:
      gender = criteria['gender']
      therapists = therapists.filter(user__gender=gender)

    if 'session_durations' in criteria:
      try:
        durations = json.loads(criteria['session_durations'])
      except:
        raise APIException("Invalid session type")

      queries = [Q(session_type=duration) for duration in durations]
      query = reduce(lambda x, y: x | y, queries)
      therapists = therapists.filter(prices__in=Price.objects.filter(query))
      
    if 'ailments' in criteria:
      ailments = json.loads(criteria['ailments'])
      therapists = therapists.filter(preferred_ailments__contains=ailments)

    if 'max_price' in criteria:
      max_price = int(criteria['max_price'])
      therapists_in_price_range = Price.objects.filter(price__lte=max_price).values('therapist')
      therapists = therapists.filter(user_id__in=therapists_in_price_range)

    # TODO there is a better way for these two, please check
    if 'review_count' in criteria:
      therapists = therapists.annotate(Count('reviews')).order_by('review_count')
    elif '-review_count' in criteria:
      therapists = therapists.annotate(Count('reviews')).order_by('-review_count')

    if 'avg_rating' in criteria:
      therapists = therapists.annotate(Avg('reviews__rating')).order_by('reviews__rating__avg')
    elif '-avg_rating' in criteria:
      therapists = therapists.annotate(Avg('reviews__rating')).order_by('-reviews__rating__avg')

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


class TherapistPricingListCreateView(generics.ListCreateAPIView):
  serializer_class = PriceSerializer

  def get_queryset(self):
    user = self.request.user
    return Price.objects.filter(therapist_id=user.id)


class TherapistPricingDetailView(generics.RetrieveUpdateDestroyAPIView):
  lookup_url_kwarg = 'price_id'
  serializer_class = PriceSerializer 

  def get_queryset(self):
    user = self.request.user
    return Price.objects.filter(therapist_id=user.id)


class TherapistCertificationListCreateView(generics.ListCreateAPIView):
  serializer_class = TherapistCertificationSerializer

  def get_queryset(self):
    user = self.request.user
    return TherapistCertification.objects.filter(therapist_id=user.id)


class TherapistCertificationDetailView(generics.RetrieveUpdateDestroyAPIView):
  lookup_url_kwarg = 'certification_id'
  serializer_class = TherapistCertificationSerializer

  def get_queryset(self):
    user = self.request.user
    return TherapistCertification.objects.filter(therapist_id=user.id)