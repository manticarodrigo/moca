from datetime import datetime

from box import Box
from django.contrib.auth import authenticate, get_user_model
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from django.db import transaction
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_serializer_method
from knox.models import AuthToken
from rest_framework import serializers, status
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework_gis.fields import GeoJsonDict

from moca.api.address.serializers import AddressSerializer
from moca.api.payment.serializers import PaymentSerializer
from moca.api.util.Validator import RequestValidator
from moca.models import (Therapist, Patient, Address, Device, AwayPeriod, Price, Certification,
                         CertificationImage, Injury, InjuryImage)
from moca.models.verification import EmailVerification
from moca.services import canned_messages
from moca.services.emails import send_email, send_verification_mail
from moca.utils.serializer_helpers import combineSerializers

from django.core import exceptions
from django.contrib.auth.password_validation import validate_password

# This is unzipping the list and takes the first list
# i.e. [(0, 1), (2, 3), (4, 5)] becomes (0, 2, 4)
SESSION_TYPES = list(zip(*Price.SESSION_TYPES))[0]

User = get_user_model()


class UserSnippetSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'first_name', 'last_name', 'image')

class UserImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('image',)

class UserSerializer(serializers.ModelSerializer):
  addresses = serializers.SerializerMethodField(read_only=True)
  payments = PaymentSerializer(read_only=True, many=True)
  email = serializers.EmailField(allow_blank=True)
  profile_info = serializers.SerializerMethodField(required=False)
  device_token = serializers.CharField(max_length=300, write_only=True, required=False)
  token = serializers.CharField(max_length=300, read_only=True)

  class Meta:
    model = User
    fields = ('id', 'first_name', 'last_name', 'gender', 'created_at', 'type', 'email', 'password',
              'is_active', 'addresses', 'payments', 'profile_info', 'image', 'device_token',
              'token')
    extra_kwargs = {
      'password': {
        'write_only': True,
        'required': False
      },
    }

  # def get_token(self, user):
  #   return AuthToken.objects.create(user)[1]

  @swagger_serializer_method(serializer_or_field=AddressSerializer(many=True))
  def get_addresses(self, user):
    addresses = Address.objects.filter(user=user, archive=False)
    serializer = AddressSerializer(instance=addresses, many=True)
    return serializer.data

  @swagger_serializer_method(serializer_or_field=combineSerializers(
    PatientProfileSerializer,
    TherapistProfileSerializer,
    serializerName=lambda a, b: 'ProfileInfo'))
  def get_profile_info(self, user):
    if user.type == User.PATIENT_TYPE:
      patient = Patient.objects.get(user=user)
      return PatientProfileSerializer(patient).data
    if user.type == User.THERAPIST_TYPE:
      therapist = Therapist.objects.get(user=user)
      return TherapistProfileSerializer(therapist).data
    return None

  def validate_email(self, email, **kwargs):
    request = self.context['request']
    user = request.user
    method = request.method
    is_update = method == 'POST' or method == 'PATCH' or 'PUT' or method == 'UPDATE'
    is_different = not hasattr(user, 'email') or email.lower() != user.email

    if email and is_update and is_different:
      existing = User.objects.filter(email__iexact=email)
      if existing.exists():
        raise serializers.ValidationError(f'Email \'{email}\' has already been registered.')

    return email

  def create(self, validated_data):
    device_token = validated_data.pop('device_token', None)
    token = validated_data.pop('token', None)
    user = User.objects.create_user(**validated_data)
    auth_token = AuthToken.objects.create(user)
    user.token = auth_token[1]

    if device_token:
      Device.objects.create(user=user, token=device_token)

    send_verification_mail(user)
    return user

  def update(self, instance, validated_data):
    if validated_data.get('password'):
      password = validated_data.pop('password')
      instance.set_password(password)
      instance.save()
    super(self.__class__, self).update(instance, validated_data)
    return instance

  def to_representation(self, obj):
    representation = super().to_representation(obj)
    profile_representation = representation.pop('profile_info')
    for key in profile_representation:
      representation[key] = profile_representation[key]

    return representation

  def validate(self, data):
    user_data = data.copy()
    user_data.pop('device_token', None)

    user = User(**user_data)
    password = user_data.get('password')

    if password:
      errors = dict()
      try:
        validate_password(password=password, user=User)
      except exceptions.ValidationError as e:
        errors['password'] = list(e.messages)

      if errors:
        raise serializers.ValidationError(errors)

    return data
