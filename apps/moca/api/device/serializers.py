from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from moca.models.user import Device, User


class DeviceSerializer(serializers.ModelSerializer):
  user = serializers.PrimaryKeyRelatedField(
        required=False,
        read_only=True,
        default=serializers.CurrentUserDefault())

  class Meta:
    model = Device
    fields = '__all__'

  def create(self, validated_data):
    validated_data['user'] = self.context['request'].user
    return Device.objects.create(**validated_data)