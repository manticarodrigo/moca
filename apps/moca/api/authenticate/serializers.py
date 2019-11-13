from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
  email = serializers.CharField()
  password = serializers.CharField()
  device_token = serializers.CharField()


# TODO Add token logic
  def validate(self, data):
    token = data['device_token']
    user = authenticate(**data)
    if user and user.is_active:
      return user
    raise serializers.ValidationError("Incorrect credentials.")
