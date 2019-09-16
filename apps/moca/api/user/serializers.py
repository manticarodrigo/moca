from datetime import datetime

from django.contrib.auth import authenticate, get_user_model
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
from django.forms import model_to_dict
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
  class Meta:
    model = User
    fields = ('id', 'first_name', 'last_name', 'gender', 'date_of_birth', 'created_at', 'type',
              'email', 'is_staff', 'is_active')
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_user):
    user = User.objects.create_user(**validated_user)
    return user


class PatientSerializer(serializers.ModelSerializer):
  class Meta:
    model = Patient
    fields = '__all__'
    depth = 1
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_patient):
    user = User.objects.create_user(**validated_patient)
    patient = Patient(user_ptr=user)
    patient.save()
    return patient


class TherapistSerializer(serializers.ModelSerializer):
  class Meta:
    model = Therapist
    fields = '__all__'
    depth = 1
    extra_kwargs = {'password': {'write_only': True}}


class UserRequestSerializer(serializers.Serializer):
  user = UserSerializer(many=False, required=False)
  # therapist = TherapistSerializer(required=True)
  addresses = AddressSerializer(many=True, required=False)
  fcmdevice_set = FCMDeviceSerializer(many=True, required=False)

  def create(self, validated):
    user = validated.pop('user')
    # TODO therapist = validated.pop('therapist')
    addresses_list = validated.pop('addresses', [])
    devices = validated.pop('fcmdevice_set', [])
    user_serializer = UserSerializer(data=user)
    user_serializer.is_valid(raise_exception=True)
    user = user_serializer.save()
    for addr in addresses_list:
      address_serializer = AddressSerializer(data=addr)
      if address_serializer.is_valid():
        location: GeoJsonDict = address_serializer.data.get("location")
        user.addresses.create(name=address_serializer.data.get('name', None),
                              text=address_serializer.data.get('text', None),
                              primary=address_serializer.data.get('primary', None),
                              location=Point(location.get("coordinates"), None),
                              apartment=address_serializer.data.get('apartment', None))

    for device in devices:
      device_serializer = FCMDeviceSerializer(data=addr)
      if device_serializer.is_valid():
        user.fcmdevice_set.create(name=device_serializer.data.get('name', None),
                                  active=device_serializer.data.get('active', True),
                                  device_id=device_serializer.data.get('device_id', None),
                                  registration_id=device_serializer.data.get(
                                    'registration_id', None),
                                  type=device_serializer.data.get('type', None))

    patient = Patient.objects.create(user=user)
    return user


def set_user_id(list_obj, user_id):
  for obj in list_obj:
    obj["user"] = user_id
  return list_obj
