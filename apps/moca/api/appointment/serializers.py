from datetime import datetime
from django.db import models
from rest_framework import serializers
from decimal import *
from moca.api.appointment.errors import AppointmentAlreadyReviewed
from moca.api.appointment.errors import AppointmentNotFound
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


class ReviewSerializer(serializers.Serializer):
  appointment_id = serializers.IntegerField(required=True)
  rating = serializers.FloatField(required=True)
  comment = serializers.CharField(required=False)

  class Meta:
    fields = '__all__'

  def validate_rating(self, value):
    getcontext().prec = 2
    value = Decimal(str(value))
    if not value <= Decimal(0) and value >= Decimal(5):
      raise serializers.ValidationError(f'rating: {value} should be between 0.0 and 5.0')
    return value

  def create(self, validated_data):
    try:
      appointment_id = validated_data.pop("appointment_id")
      appointment = Appointment.objects.get(pk=appointment_id)
    except Appointment.DoesNotExist:
      raise AppointmentNotFound(appointment_id)
    already_reviewed = Review.objects.filter(appointment_id=appointment_id)
    if already_reviewed:
      raise AppointmentAlreadyReviewed(appointment_id)
    review = appointment.review.create(rating=validated_data.get('rating'),
                                       comment=validated_data.get('comment'))
    self.calculate_therapist_rating(appointment, validated_data.get('rating'))
    return review

  def update(self, instance, validated_data):
    try:
      appointment_id = validated_data.pop("appointment_id")
      appointment = Appointment.objects.get(pk=appointment_id)
    except Appointment.DoesNotExist:
      raise AppointmentNotFound(appointment_id)
    instance.rating = validated_data.get('rating', instance.rating)
    instance.comment = validated_data.get('comment', instance.comment)
    instance.save()
    if instance.rating != validated_data.get('rating', None):
      self.calculate_therapist_rating(appointment, validated_data.get('rating'))
    return instance

  @staticmethod
  def calculate_therapist_rating(appointment, new_rating, is_deletion=False):
    getcontext().prec = 2
    therapist = appointment.therapist
    avg_rating = therapist.rating
    nb_review = therapist.review_count
    if not is_deletion:
      therapist.rating = (Decimal(str(avg_rating)) * nb_review +
                          Decimal(str(new_rating))) / (nb_review + 1)
      therapist.review_count = nb_review + 1
    else:
      if nb_review > 1:
        therapist.rating = (Decimal(str(avg_rating)) * nb_review -
                            Decimal(str(new_rating))) / (nb_review - 1)
        therapist.review_count = nb_review - 1
      else:
        therapist.rating = 0
        therapist.review_count = 0
    therapist.save()

    return
