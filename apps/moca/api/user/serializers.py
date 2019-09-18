from datetime import datetime

from django.contrib.auth import authenticate, get_user_model
from django.contrib.gis.db.models import PointField
from django.contrib.gis.geos import Point
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


class TherapistSerializer(serializers.ModelSerializer):
  class Meta:
    model = Therapist
    fields = ('bio', 'cert_date', 'operation_radius', 'qualifications', 'interests', 'status')
    depth = 1
    extra_kwargs = {'password': {'write_only': True}}


class UserRequestSerializer(serializers.Serializer):
  user = UserSerializer(many=False, required=True)
  addresses = AddressSerializer(many=True, required=False)
  fcmdevice_set = FCMDeviceSerializer(many=True, required=False)

  def create(self, validated):
    user_dict = validated.pop('user')
    print(f'ReqCreate1')
    addresses_list = validated.pop('addresses', [])
    print(f'ReqCreate2')
    devices = validated.pop('fcmdevice_set', [])
    print(f'ReqCreate3')
    user_serializer = UserSerializer(data=user_dict)
    print(f'ReqCreate4')
    user_serializer.is_valid(raise_exception=True)
    print(f'ReqCreate5')
    saved_user = user_serializer.save()
    print(f'ReqCreate6')
    saved_addresses = save_addresses(addresses_list, saved_user)
    print(f'ReqCreate7')
    saved_devices = save_devices(devices, saved_user)
    print(f'ReqCreate8')
    return saved_user, saved_addresses, saved_devices

  def update(self, existing_user, validated):
    user_dict = validated.pop('user')
    print(f'ReqUpdate0')
    addresses_list = validated.pop('addresses', [])
    print(f'ReqUpdate1')
    devices = validated.pop('fcmdevice_set', [])
    print(f'ReqUpdate2')
    user_serializer = UserSerializer(instance=existing_user, data=user_dict)
    print(f'ReqUpdate3')
    user_serializer.is_valid(raise_exception=True)
    print(f'ReqUpdate4')
    saved_user = user_serializer.save()
    print(f'ReqUpdate5')
    saved_addresses = save_addresses(addresses_list, saved_user)
    print(f'ReqUpdate6')
    saved_devices = save_devices(devices, saved_user)
    print(f'ReqUpdate7')
    return saved_user, saved_addresses, saved_devices


class PatientRequestSerializer(UserRequestSerializer):
  def create(self, validated):
    user, addresses, devices = super().create(validated)
    print(f'PatReqSer0')
    patient = Patient.objects.create(user=user)
    print(f'PatReqSer1 :{patient}')
    return user, addresses, devices, patient


class TherapistRequestSerializer(UserRequestSerializer):
  user = UserSerializer(many=False, required=True)
  therapist = TherapistSerializer(required=True)
  addresses = AddressSerializer(many=True, required=False)
  fcmdevice_set = FCMDeviceSerializer(many=True, required=False)

  def create(self, validated):
    user, addresses, devices = super().create(validated)
    therapist_dict = validated.pop('therapist')
    therapist_serializer = TherapistSerializer(data=therapist_dict)
    therapist_serializer.is_valid(raise_exception=True)
    therapist = Therapist.objects.create(user=user, **therapist_dict)
    print(f'therapist {therapist}')
    return user, addresses, devices, therapist


def save_devices(devices, user):
  saved_devices = []
  for device in devices:
    if not is_update(device):
      serializer = FCMDeviceSerializer(data=device)
      serializer.is_valid(raise_exception=True)
      saved_devices.append(
        user.fcmdevice_set.create(name=serializer.data.get('name', None),
                                  active=serializer.data.get('active', True),
                                  device_id=serializer.data.get('device_id', None),
                                  registration_id=serializer.data.get('registration_id', None),
                                  type=serializer.data.get('type', None)))
    else:
      existing_device = get_object_or_404(FCMDevice, pk=device.get('id'))
      serializer = FCMDeviceSerializer(instance=existing_device, data=device)
      serializer.save()

      # todo it looks the way below is hard way to do it
      # saved_devices.append(
      #   user.fcmdevice_set.update(
      #     name=serializer.data.get('name', existing_device.get('name')),
      #     active=serializer.data.get('active', existing_device.get('active')),
      #     device_id=serializer.data.get('device_id ', existing_device.get('device_id ')),
      #     type=serializers.data.get('type', existing_device.get('type')),
      #     registration_id=serializers.data.get('registration_id',
      #                                          existing_device.get('registration_id')),
      #   ))

  return saved_devices


def save_addresses(addresses_list, user):
  saved_addresses = []
  print(f'saveAddr0')
  for address in addresses_list:
    print(f'saveAddr1')
    if not is_update(address):
      print(f'saveAddr2')
      address_serializer = AddressSerializer(data=address)
      print(f'saveAddr3')
      address_serializer.is_valid(raise_exception=True)
      print(f'saveAddr4')
      location: GeoJsonDict = address_serializer.data.get("location")
      print(f'saveAddr5')
      saved_addresses.append(
        user.addresses.create(name=address_serializer.data.get('name', None),
                              text=address_serializer.data.get('text', None),
                              primary=address_serializer.data.get('primary', None),
                              location=Point(location.get("coordinates"), None),
                              apartment=address_serializer.data.get('apartment', None)))
      print(f'saveAddr6')
    else:
      print(f'saveAddr7')
      existing_address = get_object_or_404(Address, pk=address.get('id'))
      print(f'saveAddr8')
      serializer = AddressSerializer(instance=existing_address, data=address)
      print(f'saveAddr9')
      serializer.save()

  return saved_addresses


def is_update(a):
  try:
    address_id = a['id']
    return True
  except KeyError:
    return False
