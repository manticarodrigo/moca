from rest_framework import serializers, status

from moca.models.address import Address


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
    validated_data['user'] = self.context['request'].user
    return Address.objects.create(**validated_data)
