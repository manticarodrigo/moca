from django.contrib.auth import authenticate, get_user_model
from moca.models.user import Device
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
  email = serializers.CharField()
  password = serializers.CharField()
  device_token = serializers.CharField(required=False)

  def validate(self, data):
    device_token = data.pop('device_token', None)
    user = authenticate(**data)

    if user and user.is_active:
      if device_token:
        Device.objects.update_or_create(user=user, token=device_token)
      return user
    raise serializers.ValidationError("Incorrect credentials.")
