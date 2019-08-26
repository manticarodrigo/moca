from rest_framework import serializers
from django.contrib.auth import authenticate, get_user_model
from moca.models import Address

User = get_user_model()


class AddressSerializer(serializers.ModelSerializer):
  class Meta:
    model = Address
    fields = ('name', 'text', 'location', 'primary', 'apartment')


class UserSerializer(serializers.ModelSerializer):
  addresses = AddressSerializer(many=True)
  id = serializers.IntegerField(read_only=True)
  type = serializers.ChoiceField(choices=User.USER_TYPES, required=True)
  gender = serializers.ChoiceField(choices=User.GENDERS, required=True)

  class Meta:
    model = User
    fields = ('id', 'email', 'first_name', 'last_name', 'gender', 'date_of_birth', 'created_at',
              'type', 'addresses')
