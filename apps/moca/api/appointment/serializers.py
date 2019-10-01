from datetime import datetime
from django.db import models
from rest_framework import serializers

from moca.api.user.serializers import PatientSerializer, TherapistSerializer, AddressSerializer
from moca.models import Address, User
from moca.models.appointment import Appointment, Review
from moca.models.user import Patient, Therapist


class AppointmentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Appointment
    depth = 1
    fields = '__all__'


class AppointmentDeserializer(serializers.Serializer):

  patient = serializers.CharField(required=True)
  therapist = serializers.CharField(required=True)
  address = serializers.CharField(required=True)
  start_time = serializers.DateTimeField(required=True)
  end_time = serializers.DateTimeField(required=True)
  start_time_expected = serializers.DateTimeField(required=False)
  end_time_expected = serializers.DateTimeField(required=False)
  price = serializers.IntegerField(required=True)
  notes = serializers.CharField(required=False)
  is_cancelled = serializers.BooleanField(required=False, default=False)

  class Meta:
    fields = '__all__'

  def validate_price(self, value):
    if value <= 0:
      raise serializers.ValidationError('Price should be higher than 0')
    return value

  def validate_patient(self, value):
    try:
      patient = Patient.objects.get(user_id=value)
    except Patient.DoesNotExist:
      raise serializers.ValidationError(f'patient_id:{value} doesnt exists')
    return value

  def validate_therapist(self, value):
    try:
      therapist = Therapist.objects.get(user_id=value)
    except Therapist.DoesNotExist:
      raise serializers.ValidationError(f'therapist_id:{value} doesnt exists')
    return value

  def validate_therapist(self, value):
    address = Address.objects.get(pk=value)
    if address is None:
      raise serializers.ValidationError(f'address_id:{value} doesnt exists')
    return value

  def validate_start_time(self, value):
    if value.replace(tzinfo=None) < datetime.utcnow().replace(tzinfo=None):
      raise serializers.ValidationError(f'Start time :{value} should be a future time')
    return value

  def validate(self, data):
    if data['end_time'] < data['start_time']:
      raise serializers.ValidationError(f'End Time can not be before than Start Time')
    return data

  def create(self, validated_data):
    patient = Patient.objects.get(user_id=validated_data.pop("patient"))
    therapist = Therapist.objects.get(user_id=validated_data.pop("therapist"))
    address = Address.objects.get(id=validated_data.pop("address"))
    appointment = Appointment.objects.create(patient=patient,
                                             therapist=therapist,
                                             address=address,
                                             **validated_data)
    return appointment
    # return Appointment(address=address, **validated_data).save()

  def update(self, instance, validated_data):
    instance.start_time = validated_data.get('start_time', instance.start_time)
    instance.end_time = validated_data.get('end_time', instance.start_time)
    instance.start_time_expected = validated_data.get('start_time_expected', instance.start_time)
    instance.end_time_expected = validated_data.get('end_time_expected', instance.start_time)
    instance.notes = validated_data.get('notes', instance.notes)
    instance.modified_at = datetime.now()
    instance = instance.save()
    return instance


class ReviewSerializer(serializers.ModelSerializer):
  # appointment = serializers.IntegerField(required=True)
  # rating = serializers.IntegerField(required=True)
  # comment = serializers.CharField(required=False)
  class Meta:
    model = Review
    fields = '__all__'

  # todo activate validations for inputs
  # def validate_rating(self, value):
  #   if 0 > value > 5:
  #     return serializers.ValidationError(f'rating: {value} should be between 0 and 5')

  #
  # def validate_comment(self, value):
  #   self.comment = value

  # def create(self, validated_data):
  #   # appointment_id = validated_data.get("appointment")
  #   # print(f'========> in create : appointmentid {self.appointment} rating:{self.rating}')
  #   appointment = Appointment.objects.get(id=validated_data.pop('appointment'))
  #   print(f'========> in create : {appointment}')
  #   review = ReviewSerializer(data=validated_data)
  #   review.is_valid(raise_exception=True)
  #   review.save()
  #   appointment.review_set = review
  #   return review
