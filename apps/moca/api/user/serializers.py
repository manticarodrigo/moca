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
from moca.models import Price, Injury, TherapistCertification
from moca.models.address import Address
from moca.models.user import Patient, Therapist, AwayDays
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


class LeaveSerializer(serializers.ModelSerializer):
  class Meta:
    model = AwayDays
    exclude = ['therapist']

  def create(self, validated_data):
    request = self.context['request']
    user_id = request.user.id
    away_days = AwayDays.objects.create(therapist_id=user_id,
                                        start_date=validated_data.get('start_date'),
                                        end_date=validated_data.get('end_date'))
    return away_days

  def validate_therapist(self, value):
    RequestValidator.therapist(value)
    return value

  def validate_start_date(self, value):
    RequestValidator.future_date(value)
    return value

  def validate(self, data):
    start_date = data['start_date']
    end_date = data['end_date']
    RequestValidator.end_after_start(end_date, start_date)
    return data


class InjurySerializer(serializers.ModelSerializer):
  class Meta:
    model = Injury
    fields = '__all__'


class TherapistCertificationSerializer(serializers.ModelSerializer):
  therapist = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = TherapistCertification
    fields = '__all__'

  def create(self, validated_data):
    user = self.context['request'].user
    validated_data['therapist_id'] = user.id
    return super(TherapistCertificationSerializer, self).create(validated_data)


class PriceSerializer(serializers.ModelSerializer):
  therapist = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = Price
    fields = ('id', 'therapist', 'session_type', 'price')

  def create(self, validated_data):
    validated_data['therapist'] = Therapist.objects.get(user=self.context['request'].user)
    price = validated_data.pop('price')
    Price.objects.filter(**validated_data).delete()
    return Price.objects.create(**validated_data, price=price)

  def validate_session_type(self, session_type):
    if session_type not in SESSION_TYPES:
      raise serializers.ValidationError(f"Invalid session type should be one of {SESSION_TYPES}")
    return session_type


class PatientProfileSerializer(serializers.ModelSerializer):
  injury = InjurySerializer(read_only=True)

  class Meta:
    model = Patient
    fields = ['injury']


class TherapistProfileSerializer(serializers.ModelSerializer):
  prices = PriceSerializer(many=True, required=False)
  certifications = TherapistCertificationSerializer(many=True, required=False)
  away_days = LeaveSerializer(many=True, required=False)

  class Meta:
    model = Therapist
    exclude = ['user']


class UserSnippetSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ('id', 'first_name', 'last_name', 'image')


class UserSerializer(serializers.ModelSerializer):
  addresses = AddressSerializer(read_only=True, many=True)
  payments = PaymentSerializer(read_only=True, many=True)
  email = serializers.EmailField(allow_blank=True)
  profile_info = serializers.SerializerMethodField(required=False)

  class Meta:
    model = User
    fields = ('id', 'first_name', 'last_name', 'gender', 'created_at', 'type', 'email', 'password',
              'is_active', 'addresses', 'payments', 'profile_info', 'image')
    extra_kwargs = {
      'password': {
        'write_only': True,
        'required': False
      },
    }

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
    user = User.objects.create_user(**validated_data)
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
    user = User(**data)
    password = data.get('password')

    if password:
      errors = dict()
      try:
        validate_password(password=password, user=User)
      except exceptions.ValidationError as e:
        errors['password'] = list(e.messages)

      if errors:
        raise serializers.ValidationError(errors)

    return data


class PatientSerializer(serializers.ModelSerializer):
  user = UserSerializer()
  injury = InjurySerializer(required=False)

  class Meta:
    model = Patient
    fields = '__all__'

  def to_representation(self, obj):
    representation = super().to_representation(obj)
    user_representation = representation.pop('user')
    for key in user_representation:
      representation[key] = user_representation[key]

    return representation

  @transaction.atomic
  def update(self, instance, validated_data):
    user_data = validated_data.pop('user', None)
    if user_data:
      user_serializer = UserSerializer(instance=instance.user, data=user_data, partial=True,
                                       context=self.context)

      if user_serializer.is_valid():
        user_serializer.save()

    injury_data = validated_data.pop('injury', None)
    if injury_data:
      if hasattr(instance, 'injury'):
        injury_serializer = InjurySerializer(instance=instance.injury,
                                             data=injury_data,
                                             partial=True)
      else:
        injury_data['patient'] = instance
        injury_serializer = InjurySerializer(data=injury_data)

      if injury_serializer.is_valid():
        instance.injury = injury_serializer.save()
      else:
        raise APIException('Invalid Injury')

    instance.save()

    return instance


class PatientCreateSerializer(PatientSerializer):
  token = serializers.SerializerMethodField()

  def get_token(self, patient):
    return AuthToken.objects.create(patient.user)[1]

  @transaction.atomic
  def create(self, validated_data):
    validated_data['user']['type'] = User.PATIENT_TYPE
    user = UserSerializer(context=self.context).create(validated_data.pop('user'))
    return Patient.objects.create(user=user, **validated_data)


class TherapistSearchSerializer(serializers.ModelSerializer):
  user = UserSnippetSerializer()
  prices = PriceSerializer(many=True)

  class Meta:
    model = Therapist
    fields = ['license_number', 'rating', 'user', 'prices']

  def to_representation(self, obj):
    representation = super().to_representation(obj)
    user_representation = representation.pop('user')
    for key in user_representation:
      representation[key] = user_representation[key]

    return representation


class TherapistSerializer(serializers.ModelSerializer):
  user = UserSerializer()
  prices = PriceSerializer(many=True, required=False)
  certifications = TherapistCertificationSerializer(many=True, required=False)

  class Meta:
    model = Therapist
    fields = '__all__'

  def to_representation(self, obj):
    representation = super().to_representation(obj)
    user_representation = representation.pop('user')
    for key in user_representation:
      representation[key] = user_representation[key]

    return representation

  def update(self, instance, validated_data):
    if validated_data.get('user'):
      user_data = validated_data.pop('user')
      user_serializer = UserSerializer(instance=instance.user, data=user_data, partial=True,
                                       context=self.context)
      if user_serializer.is_valid():
        user_serializer.save()

    # therapist fields
    instance.bio = validated_data.get('bio', instance.bio)
    instance.status = validated_data.get('status', instance.status)
    instance.cert_date = validated_data.get('cert_date', instance.cert_date)
    instance.license_number = validated_data.get('license_number', instance.license_number)
    instance.operation_radius = validated_data.get('operation_radius', instance.operation_radius)
    instance.preferred_ailments = validated_data.get('preferred_ailments',
                                                     instance.preferred_ailments)

    instance.save()

    return instance


class TherapistCreateSerializer(TherapistSerializer):
  token = serializers.SerializerMethodField()

  def get_token(self, therapist):
    return AuthToken.objects.create(therapist.user)[1]

  def create(self, validated_data):
    validated_data['user']['type'] = User.THERAPIST_TYPE
    user = UserSerializer(context=self.context).create(validated_data['user'])
    return Therapist.objects.create(user=user)
