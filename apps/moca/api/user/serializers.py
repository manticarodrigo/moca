from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from moca.models import Address
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
        fields = '__all__'
        depth = 1
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated):
        addresses = validated.pop('addresses')
        fcm_device = validated.pop('fcmdevice_set')
        user = User.objects.create_user(**validated)
        for address in addresses:
            print('in user create while running create')
            address = Address.objects.create(user=user, **address)
            user.addresses.add(address)

        for device in fcm_device:
            device = FCMDevice.objects.create(**device)
            user.fcmdevice_set.add(device)
        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.save()
        return instance
