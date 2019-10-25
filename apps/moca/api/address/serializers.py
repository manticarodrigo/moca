from rest_framework import serializers, status
from rest_framework.exceptions import APIException

from moca.models.address import Address
from moca.models.app_availability import Area
from moca.models.user import Therapist, User
from moca.services import canned_messages
from moca.services.emails import send_email


class AddressSerializer(serializers.ModelSerializer):
  class Meta:
    model = Address
    exclude = ['user']

  def update(self, instance, validated_data):
    if validated_data['primary']:
      addresses = Address.objects.filter(user_id=instance.user_id)
      for address in addresses:
        address.primary = False
        address.save()

    return super(AddressSerializer, self).update(instance, validated_data)

  def create(self, validated_data):
    user = self.context['request'].user
    validated_data['user'] = user

    if validated_data['primary']:
      addresses = Address.objects.filter(user=user)
      for address in addresses:
        address.primary = False
        address.save()

      if user.type == User.THERAPIST_TYPE:
        therapist = Therapist.objects.get(user=user)
        therapist.primary_location = validated_data['location']
        therapist.save()

    if not Area.objects.filter(zip_code=validated_data['zip_code']).exists():
      if user.type == User.PATIENT_TYPE:
        send_email(user, **canned_messages.PATIENT_UNAVAILABLE)
      elif user.type == User.THERAPIST_TYPE:
        send_email(user, **canned_messages.THERAPIST_UNAVAILABLE)

      UnavailableArea.objects.create(email=user.email, zip_code=validated_data['zip_code'])
      raise APIException("Zip code is unavailable")

    return Address.objects.create(**validated_data)
