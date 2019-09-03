from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from moca.models import Address
from fcm_django.models import FCMDevice

User = get_user_model()


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = ['user']


class FCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        exclude = ['user']


class UserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, required=True)
    fcmdevice_set = FCMDeviceSerializer(many=True, required=True)

    class Meta:
        model = User
        fields = '__all__'
        depth = 1
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated):
        addresses = validated.pop('addresses')
        fcm_device = validated.pop('fcmdevice_set')
        user = User.objects.create_user(**validated)
        for address in addresses:
            address = Address.objects.create(user=user, **address)
            user.addresses.add(address)

        for device in fcm_device:
            device = FCMDevice.objects.create(**device)
            user.fcmdevice_set.add(device)
        return user
