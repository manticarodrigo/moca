import datetime

from rest_framework import serializers

from moca.models import Patient, Therapist, Address


class RequestValidator:
  @staticmethod
  def future_date(value):
    if value < datetime.date.today():
      raise serializers.ValidationError(f'Start Day :{value} cant be past day')

  @staticmethod
  def future_time(value):
    if value.replace(tzinfo=None) < datetime.datetime.utcnow().replace(tzinfo=None):
      raise serializers.ValidationError(f'Start time :{value} should be a future time')

  @staticmethod
  def end_after_start(end, start):
    if end < start:
      raise serializers.ValidationError(f'{end} can not be before than {start}')

  @staticmethod
  def address_belongs_to_user(address_id, user_id):
    address = Address.objects.filter(user_id__exact=user_id).filter(id=address_id)
    if not address:
      raise serializers.ValidationError(
        f'Address Id: {address_id} doesnt belong to user Id: {user_id}')
