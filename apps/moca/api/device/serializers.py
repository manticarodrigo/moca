from django.contrib.auth import authenticate, get_user_model
from rest_framework import serializers

from moca.models.user import Device


class DeviceSerializer(serializers.ModelSerializer):
  user = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = Device
    fields = '__all__'

  def create(self, validated_data):
    validated_data['user'] = self.context['request'].user
    return Device.objects.create(**validated_data)