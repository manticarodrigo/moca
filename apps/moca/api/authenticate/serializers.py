from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
  email = serializers.CharField()
  password = serializers.CharField()
  device_token = serializers.CharField(required=False)

  def validate(self, data):
    user = authenticate(**data)

    if user and user.is_active:
      return user
    raise serializers.ValidationError("Incorrect credentials.")
