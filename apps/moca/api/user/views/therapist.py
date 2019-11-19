import json
from functools import reduce

from django.db.models import Avg, Count, F, Q
from rest_framework import generics
from rest_framework.exceptions import APIException
from rest_framework.parsers import MultiPartParser

from moca.models import Therapist, Address, Price, AwayPeriod, Certification

from ..permissions import IsObjectUserSelfOrReadonly, IsObjectTherapistSelfOrReadonly
from ..serializers import (TherapistSerializer, TherapistCreateSerializer,
                           TherapistSearchSerializer, CertificationSerializer, PriceSerializer,
                           AwayPeriodSerializer)


class TherapistCreateView(generics.CreateAPIView):
  serializer_class = TherapistCreateSerializer
  permission_classes = []


class TherapistDetailView(generics.RetrieveUpdateAPIView):
  serializer_class = TherapistSerializer
  queryset = Therapist.objects
  permission_classes = [IsObjectUserSelfOrReadonly]


class TherapistCertificationCreateView(generics.CreateAPIView):
  serializer_class = CertificationSerializer
  queryset = Certification.objects
  permission_classes = [IsObjectTherapistSelfOrReadonly]
  parser_classes = (MultiPartParser,)


class TherapistCertificationDetailView(generics.RetrieveUpdateDestroyAPIView):
  lookup_url_kwarg = 'certification_id'
  serializer_class = CertificationSerializer
  queryset = Certification.objects
  permission_classes = [IsObjectTherapistSelfOrReadonly]
  parser_classes = (MultiPartParser,)

class TherapistSearchView(generics.ListAPIView):
  serializer_class = TherapistSearchSerializer
  queryset = Therapist.objects.annotate(Count('prices')).filter(prices__count__gt=0)

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


class TherapistAwayPeriodListCreateView(generics.ListCreateAPIView):
  serializer_class = AwayPeriodSerializer
  permission_classes = [IsObjectTherapistSelfOrReadonly]

  def get_queryset(self):
    user = self.request.user
    return AwayPeriod.objects.filter(therapist_id=user.id)


class TherapistAwayPeriodDetailView(generics.RetrieveUpdateDestroyAPIView):
  lookup_url_kwarg = 'period_id'
  serializer_class = AwayPeriodSerializer
  permission_classes = [IsObjectTherapistSelfOrReadonly]

  def get_queryset(self):
    user = self.request.user
    return AwayPeriod.objects.filter(therapist_id=user.id)


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
