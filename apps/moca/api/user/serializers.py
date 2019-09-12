from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers
from moca.models.user import User, Patient, Therapist
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


class PatientSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, required=False)
    fcmdevice_set = FCMDeviceSerializer(many=True, required=False)

    class Meta:
        model = Patient
        fields = '__all__'
        depth = 1
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated: User):
        user: User
        saved_addresses = Address.objects.create_user_addresses(validated)
        self.create_user_devices(user, validated)

        user = User.objects.create_user(**validated)
        return user


    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.date_of_birth = validated_data.get('date_of_birth', instance.date_of_birth)
        instance.save()
        return instance
