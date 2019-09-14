from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from moca.models.user import User, Patient, Therapist
from rest_framework.response import Response
from rest_framework import status
from moca.models.address import Address
from fcm_django.models import FCMDevice

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
  fcmdevice_set = FCMDeviceSerializer(many=True, required=False)

  class Meta:
    model = User
    fields = ('id', 'first_name', 'last_name', 'gender', 'date_of_birth', 'created_at', 'type',
              'email', 'is_staff', 'is_active', 'addresses', 'fcmdevice_set')
    depth = 1
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated_user):
    print(f'validated_user : {validated_user}')
    print('serializer create0')
    addrs = []
    devices = []
    if validated_user.get('addresses') is not None:
      addrs = validated_user.pop('addresses')

    if validated_user.get('fcmdevice_set') is not None:
      devices = validated_user.pop('fcmdevice_set')
    print(f'serializer create4 {validated_user}')
    if validated_user.get('type') == 'PA':
      user = Patient.objects.create(user=validated_user)
    else:
      user = Patient.objects.create(user=validated_user)

    print(f'userid : {user.id}')
    print('serializer create5')
    if addrs is not None:
      set_user_id(addrs, user.id)
    if devices is not None:
      set_user_id(devices, user.id)

    print('serializer create6')
    for addr in addrs:
      print('serializer create7')
      address_serializer = AddressSerializer(data=addr)
      print('serializer create8')
      if address_serializer.is_valid():
        print('serializer create9')
        address_serializer.save()
      else:
        # todo test invalid cases of adresses.
        return Response(address_serializer.errors, status.HTTP_400_BAD_REQUEST)

    for device in devices:
      device_serializer = FCMDeviceSerializer(data=device)
      if device_serializer.is_valid():
        device_serializer.save()
      else:
        # todo test invalid cases of devices.
        return Response(device_serializer.errors, status.HTTP_400_BAD_REQUEST)
    print('serializer create10')
    address_serializer.save()
    return user

  def update(self, instance, validated_data):
    instance.first_name = validated_data.get('first_name', instance.first_name)
    instance.last_name = validated_data.get('last_name', instance.last_name)
    instance.gender = validated_data.get('gender', instance.gender)
    instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
    instance.save()
    return instance


class PatientSerializer(UserSerializer):
  def __str__(self):
    return get_user_model().id


additional_fields = (
  'bio',
  'cert_date',
  'operation_radius',
  'qualifications',
  'interests',
  'status',
)


class TherapistSerializer(UserSerializer):
  class Meta:
    model = Therapist
    fields = UserSerializer.Meta.fields + additional_fields
    depth = 1
    extra_kwargs = {'password': {'write_only': True}}

  def create(self, validated):
    therapist = {}
    print(f'validated : {validated}')
    for field in additional_fields:
      therapist[field] = validated.pop(field, None)
    # setattr(therapist, field, validated.pop(field, None))
    user_serializer = UserSerializer(data=validated)
    user_serializer.is_valid(raise_exception=True)
    user = user_serializer.save()
    print(f'therasera5 <user> : {user}')
    therapist = Therapist.objects.create(**therapist)
    return therapist


def set_user_id(list_obj, user_id):
  print('in setuser0')
  for obj in list_obj:
    obj["user"] = user_id
  return list_obj
