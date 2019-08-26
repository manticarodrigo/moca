from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from moca.models import Address

User = get_user_model()


class AddressSerializer(serializers.ModelSerializer):
  class Meta:
    model = Address
    fields = ('name', 'text', 'location')


class UserSerializer(serializers.ModelSerializer):
  addresses = AddressSerializer(read_only=True, many=True)

  class Meta:
    model = User
    fields = ('id', 'email', 'addresses')
