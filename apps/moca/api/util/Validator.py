import datetime

from rest_framework import serializers

from moca.models import Patient, Therapist, Address


class RequestValidator:
  @staticmethod
  def patient(value):
    try:
      patient = Patient.objects.get(user_id=value)
    except Patient.DoesNotExist:
      raise serializers.ValidationError(f'patient_id:{value} doesnt exists')

  @staticmethod
  def therapist(value):
    try:
      therapist = Therapist.objects.get(user_id=value)
    except Therapist.DoesNotExist:
      raise serializers.ValidationError(f'therapist_id:{value} doesnt exists')

  @staticmethod
  def address(value):
    address = Address.objects.get(pk=value)
    if address is None:
      raise serializers.ValidationError(f'address_id:{value} doesnt exists')

  @staticmethod
  def future_date(value):
    if value < datetime.date.today():
      raise serializers.ValidationError(f'Start Day :{value} cant be past day')

  @staticmethod
  def future_time(value):
    if value.replace(tzinfo=None) < datetime.datetime.utcnow().replace(tzinfo=None):
      raise serializers.ValidationError(f'Start time :{value} should be a future time')

  @staticmethod
  def end_after_start(data, end, start):
    if data[end] < data[start]:
      raise serializers.ValidationError(f'{end} can not be before than {start}')
