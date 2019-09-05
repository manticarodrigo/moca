from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from moca.models import Address
from fcm_django.models import FCMDevice

User = get_user_model()


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

    def create(self, validated_data):
        return Address.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.text = validated_data.get('text', instance.text)
        instance.primary = validated_data.get('primary', instance.primary)
        instance.apartment = validated_data.get('apartment', instance.apartment)
        instance.location = validated_data.get('location', instance.location)
        instance.user = validated_data.get('user', instance.user)
        instance.save()
        return instance


class FCMDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMDevice
        exclude = ['user']

    def create(self, validated_data):
        return FCMDevice.objects.create(**validated_data)

    def update(self, instance, validated_data):
        print(instance.user)
        instance.registration_id = validated_data.get('registration_id', instance.registration_id)
        instance.name = validated_data.get('name', instance.name)
        instance.active = validated_data.get('active', instance.active)
        instance.user = validated_data.get('user', instance.user)
        instance.device_id = validated_data.get('device_id', instance.device_id)
        instance.type = validated_data.get('type', instance.type)
        instance.save()
        return instance


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
            address = Address.objects.create(user=user, **address)
            user.addresses.add(address)

        for device in fcm_device:
            device = FCMDevice.objects.create(**device)
            user.fcmdevice_set.add(device)
        return user


class UserSerializerForUpdate(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, required=True)
    fcmdevice_set = FCMDeviceSerializer(many=True, required=True)

    class Meta:
        model = User
        fields = '__all__'
        depth = 1
