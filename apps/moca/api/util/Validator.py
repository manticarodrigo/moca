import datetime

from django.utils import timezone
from rest_framework import serializers

from moca.models import Address


class RequestValidator:
  @staticmethod
  def future_date(value):
    if value < timezone.now():
      raise serializers.ValidationError(f'Start day cant be a past date.')

  @staticmethod
  def future_time(value):
    if value.replace(tzinfo=None) < datetime.datetime.utcnow().replace(tzinfo=None):
      raise serializers.ValidationError(f'Start time should be a future time.')

  @staticmethod
  def end_after_start(end, start):
    if end < start:
      raise serializers.ValidationError(f'End time can not be before start time.')

  @staticmethod
  def address_belongs_to_user(address_id, user_id):
    address = Address.objects.filter(user_id__exact=user_id).filter(id=address_id)
    if not address:
      raise serializers.ValidationError(f'Address does not belong to user.')
