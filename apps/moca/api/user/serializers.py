from datetime import datetime

from django.contrib.auth import authenticate, get_user_model
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from django.db import transaction
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from fcm_django.models import FCMDevice
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework_gis.fields import GeoJsonDict

from moca.models.address import Address
from moca.models.user import Patient, Therapist, User

User = get_user_model()


class AddressSerializer(serializers.ModelSerializer):
  class Meta:
    model = Address
    fields = '__all__'


class FCMDeviceSerializer(serializers.ModelSerializer):
  class Meta:
    model = FCMDevice
    fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
  addresses = AddressSerializer(many=True, required=False)

  class Meta:
    model = User
    fields = ('id', 'first_name', 'last_name', 'gender', 'date_of_birth', 'created_at', 'type',
              'email', 'is_staff', 'is_active', 'password', 'addresses')
    extra_kwargs = {
      'password': {
        'write_only': True,
        'required': True
      },
      'gender': {
        'required': True
      }
    }


class PatientSerializer(serializers.ModelSerializer):
  user = UserSerializer()

  class Meta:
    model = Patient
    fields = '__all__'
    depth = 2


class TherapistSerializer(serializers.ModelSerializer):
  user = UserSerializer(required=False)

  class Meta:
    model = Therapist
    fields = ('bio', 'cert_date', 'operation_radius', 'qualifications', 'interests', 'status',
              'user')


class UserRequestSerializer(serializers.Serializer):
  user = UserSerializer(many=False, required=True)
  addresses = AddressSerializer(many=True, required=False)
  fcmdevice_set = FCMDeviceSerializer(many=True, required=False)

  @transaction.atomic
  def create(self, validated):
    user = User.objects.create_user(**validated.pop("user"))

    addresses = AddressSerializer(data=validated.pop("addresses"), many=True)
    addresses.is_valid(raise_exception=True)
    addresses = addresses.save()
    user.addresses.set(addresses)

    fcmdevices = FCMDeviceSerializer(data=validated.pop("fcmdevice_set"), many=True)
    fcmdevices.is_valid(raise_exception=True)
    fcmdevices.save()
    user.fcmdevice_set_set = fcmdevices

    user.save()

    return user


class PatientRequestSerializer(serializers.Serializer):
  user = UserSerializer()
  addresses = AddressSerializer(many=True, required=False)
  fcmdevice_set = FCMDeviceSerializer(many=True, required=False)

  def create(self, validated):
    validated['user']['type'] = User.PATIENT
    user = UserRequestSerializer(data=validated)
    user.is_valid(raise_exception=True)

    patient = Patient.objects.create(user=user.save())
    patient.save()
    return patient


class TherapistRequestSerializer(serializers.Serializer):
  user = UserSerializer(many=False, required=True)
  therapist = TherapistSerializer(required=True)
  addresses = AddressSerializer(many=True, required=False)
  fcmdevice_set = FCMDeviceSerializer(many=True, required=False)

  def create(self, validated):
    therapist = validated.pop('therapist')

    validated['user']['type'] = User.THERAPIST

    user = UserRequestSerializer(data=validated)
    user.is_valid(raise_exception=True)
    user = user.save()

    lng, lat = AddressSerializer(user.addresses.get(primary=True)).data['location']['coordinates']

    therapist['primary_location'] = Point(lng, lat)

    return Therapist.objects.create(user=user, **therapist)
