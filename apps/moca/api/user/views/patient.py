import json
from functools import reduce

from django.db.models import Avg, Count, F, Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from drf_yasg import openapi
from drf_yasg.inspectors import SwaggerAutoSchema
from drf_yasg.utils import swagger_auto_schema

from moca.models import (User, Therapist, Patient, Address, Price, EmailVerification, AwayPeriod,
                         Certification, Injury)
from moca.services import canned_messages
from moca.services.emails import send_email

from ..permissions import IsUserSelf, IsObjectUserSelfOrReadonly, IsObjectPatientSelfOrReadonly
from ..serializers import (UserSerializer, UserImageSerializer, AwayPeriodSerializer,
                          TherapistSerializer, TherapistCreateSerializer, CertificationSerializer,
                          PriceSerializer, TherapistSearchSerializer, PatientSerializer,
                          PatientCreateSerializer, InjurySerializer)


class PatientCreateView(generics.CreateAPIView):
  serializer_class = PatientCreateSerializer
  permission_classes = []


class PatientDetailView(generics.RetrieveUpdateAPIView):
  serializer_class = PatientSerializer
  queryset = Patient.objects
  permission_classes = [IsObjectUserSelfOrReadonly]


# TODO: fix collectionFormat='multi' (yasg works, openapi-generator doesn't)
#
# images_param = openapi.Parameter(name='images', in_=openapi.IN_FORM, required=False,
#                                  type=openapi.TYPE_ARRAY, collectionFormat='multi',
#                                  items=openapi.Items(type=openapi.TYPE_FILE))

class PatientInjuryCreateView(generics.CreateAPIView):
  serializer_class = InjurySerializer
  queryset = Injury.objects
  permission_classes = [IsObjectPatientSelfOrReadonly]
  parser_classes = (MultiPartParser,)


class PatientInjuryDetailView(generics.RetrieveUpdateDestroyAPIView):
  lookup_url_kwarg = 'injury_id'
  serializer_class = InjurySerializer
  queryset = Injury.objects
  permission_classes = [IsObjectPatientSelfOrReadonly]
  parser_classes = (MultiPartParser,)
