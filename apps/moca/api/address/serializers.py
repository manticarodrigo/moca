from rest_framework import serializers, status

from moca.models.address import Address
from moca.models.user import Therapist, User
from moca.models.app_availability import Area
from moca.services.emails import send_email
from moca.services import canned_messages


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

    if not Area.objects.filter(state=address['state'], zip_code=address['zip_code']).exists():
      if user.type == User.PATIENT_TYPE:
        send_email(user, **canned_messages.PATIENT_UNAVAILABLE)
      elif user.type == User.THERAPIST_TYPE:
        send_email(user, **canned_messages.THERAPIST_UNAVAILABLE)

    return Address.objects.create(**validated_data)
