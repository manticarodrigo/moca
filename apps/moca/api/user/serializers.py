from box import Box
from datetime import datetime
from knox.models import AuthToken

from django.contrib.auth import authenticate, get_user_model
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from django.db import transaction
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework_gis.fields import GeoJsonDict

from moca.api.util.Validator import RequestValidator
from moca.api.address.serializers import AddressSerializer
from moca.api.payment.serializers import PaymentSerializer 
from moca.models.user import Patient, Therapist
from moca.models import Price
from moca.models.address import Address
from moca.models.user.user import AwayDays

from .errors import DuplicateEmail

SESSION_TYPES = ['thirty', 'fourtyfive', 'sixty', 'evaluation']

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
  addresses = AddressSerializer(read_only=True, many=True)
  payments = PaymentSerializer(read_only=True, many=True)
  email = serializers.EmailField(allow_blank=True)

  class Meta:
    model = User
    fields = ('id', 'first_name', 'last_name', 'gender', 'created_at', 'type',
              'email', 'password', 'is_active', 'addresses', 'payments')
    extra_kwargs = {
      'password': {
        'write_only': True,
        'required': False
      },
    }

  def get_request_method(self):
    context = Box(self.context)

    return context.request._request.environ['REQUEST_METHOD']

  def validate_email(self, email, **kwargs):
    is_post_request = self.get_request_method() == 'POST'

    if email and is_post_request:
      existing = User.objects.filter(email__iexact=email)

      if existing.exists():
        raise DuplicateEmail(email)

    return email

  def create(self, validated_data):
    user = User.objects.create_user(**validated_data)

    return user

class PatientSerializer(serializers.ModelSerializer):
  user = UserSerializer()

  class Meta:
    model = Patient
    fields = '__all__'
  
  def update(self, instance, validated_data):
    user = validated_data.get('user', instance.user.__dict__)

    # user fields
    instance.user.email = user.get('email')
    instance.user.first_name = user.get('first_name')
    instance.user.last_name = user.get('last_name')
    instance.user.gender = user.get('gender')

    password = validated_data.get('user', {}).get('password')

    if password:
      instance.user.set_password(password)

    instance.user.save()
    instance.save()

    return instance

class PatientCreateSerializer(PatientSerializer):
  token = serializers.SerializerMethodField()

  def get_token(self, patient):
    return AuthToken.objects.create(patient.user)[1]

  def create(self, validated_data):
    validated_data['user']['type'] = User.PATIENT
    user = UserSerializer().create(validated_data['user'])
    return Patient.objects.create(user=user)

class TherapistSerializer(serializers.ModelSerializer):
  user = UserSerializer()

  class Meta:
    model = Therapist
    fields = '__all__'

  def update(self, instance, validated_data):
    user = validated_data.get('user', instance.user.__dict__)

    # user fields
    instance.user.email = user.get('email')
    instance.user.first_name = user.get('first_name')
    instance.user.last_name = user.get('last_name')
    instance.user.gender = user.get('gender')

    # therapist fields
    instance.bio = validated_data.get('bio', instance.bio)
    instance.cert_date = validated_data.get('cert_date', instance.cert_date)
    instance.license_number = validated_data.get('license_number', instance.license_number)
    instance.operation_radius = validated_data.get('operation_radius', instance.operation_radius)
    instance.qualifications = validated_data.get('qualifications', instance.qualifications)
    instance.preferred_ailments = validated_data.get('preferred_ailments', instance.preferred_ailments)

    password = validated_data.get('user', {}).get('password')

    if password:
      instance.user.set_password(password)

    instance.user.save()
    instance.save()

    return instance
  
class TherapistCreateSerializer(TherapistSerializer):
  token = serializers.SerializerMethodField()

  def get_token(self, therapist):
    return AuthToken.objects.create(therapist.user)[1]

  def create(self, validated_data):
    validated_data['user']['type'] = User.THERAPIST
    user = UserSerializer().create(validated_data['user'])
    return Therapist.objects.create(user=user)

class PriceSerializer(serializers.ModelSerializer):
  therapist = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = Price
    fields = ('therapist', 'session_type', 'price')

  def create(self, validated_data):
    validated_data['therapist'] = Therapist.objects.get(user=self.context['request'].user)
    price = validated_data.pop('price')
    Price.objects.filter(**validated_data).delete()
    return Price.objects.create(**validated_data, price=price)

  def validate_session_type(self, session_type):
    if session_type not in SESSION_TYPES:
      raise serializers.ValidationError(f"Invalid session type should be one of {SESSION_TYPES}")
    return session_type

class LeaveSerializer(serializers.Serializer):
  therapist = serializers.IntegerField(required=True)
  start_date = serializers.DateField(required=True)
  end_date = serializers.DateField(required=True)

  class Meta:
    fields = '__all__'

  def create(self, validated):
    therapist = Therapist.objects.get(user_id=validated.pop('therapist'))
    awaydays = therapist.awaydays.create(start_date=validated.get('start_date'),
                                         end_date=validated.get('end_date'))
    return awaydays

  def validate_therapist(self, value):
    RequestValidator.therapist(value)
    return value

  def validate_start_date(self, value):
    RequestValidator.future_date(value)
    return value

  def validate(self, data):
    RequestValidator.end_after_start(data, 'end_date', 'start_date')
    return data

class LeaveResponseSerializer(serializers.Serializer):
  id = serializers.IntegerField(required=False)
  therapist = TherapistSerializer(required=True)
  start_date = serializers.DateField(required=True)
  end_date = serializers.DateField(required=True)

  class Meta:
    fields = '__all__'
    depth = 1
