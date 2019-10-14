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
from moca.models.user import Patient, Therapist
from moca.models import Price
from moca.models.user.user import AwayDays
from moca.models.address import Address

SESSION_TYPES = ['thirty', 'fourtyfive', 'sixty', 'evaluation']


class AddressSerializer(serializers.ModelSerializer):
  user = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = Address
    fields = '__all__'
  
  def create(self, validated_data):
    validated_data['user'] = self.context['request'].user
    return Address.objects.create(**validated_data)


User = get_user_model()

class UserSerializer(serializers.ModelSerializer):

  class Meta:
    model = User
    fields = ('id', 'first_name', 'last_name', 'gender', 'created_at', 'type',
              'email', 'password', 'is_active')
    extra_kwargs = {
      'password': {
        'write_only': True,
        'required': True
      }
    }

  def create(self, validated_data):
    user = User.objects.create_user(**validated_data)
    return user

  def update(self, instance, validated_data):
    password = validated_data.pop("password")
    instance.__dict__.update(validated_data)
    if password:
      instance.set_password(password)
      instance.save()
    return instance


class PatientSerializer(serializers.ModelSerializer):
  user = UserSerializer()

  class Meta:
    model = Patient
    fields = '__all__'
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


class TherapistCreateSerializer(TherapistSerializer):
  token = serializers.SerializerMethodField()

  def get_token(self, therapist):
    return AuthToken.objects.create(therapist.user)[1]

  def create(self, validated_data):
    validated_data['user']['type'] = User.THERAPIST
    user = UserSerializer().create(validated_data['user'])
    return Therapist.objects.create(user=user)


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
