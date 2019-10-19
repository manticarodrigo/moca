from rest_framework import serializers, status

from moca.models.address import Address
from moca.models.user import Therapist


class AddressSerializer(serializers.ModelSerializer):
  class Meta:
    model = Address
    exclude = ['user']


class AddressCreateSerializer(serializers.ModelSerializer):
  user = serializers.PrimaryKeyRelatedField(read_only=True)

  class Meta:
    model = Address
    fields = '__all__'

  def create(self, validated_data):
    user = self.context['request'].user
    validated_data['user'] = user

    if validated_data['primary'] and user.type == 'PT':
      therapist = Therapist.objects.get(user_id=user.id)
      therapist.primary_location = validated_data['location']
      therapist.save()

    return Address.objects.create(**validated_data)
