from datetime import datetime
from django.db import models, transaction
from rest_framework import serializers
from decimal import *
from moca.api.appointment.errors import AppointmentAlreadyReviewed
from moca.api.appointment.errors import AppointmentNotFound
from moca.api.user.serializers import PatientSerializer, TherapistSerializer, AddressSerializer
from moca.models import Address, User
from moca.models.appointment import Appointment, Review
from moca.models.user import Patient, Therapist
from enum import *


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

  def validate_start_time(self, value):
    if value.replace(tzinfo=None) < datetime.utcnow().replace(tzinfo=None):
      raise serializers.ValidationError(f'Start time :{value} should be a future time')
    return value

  def validate_end_time(self, value):
    if value.replace(tzinfo=None) < datetime.utcnow().replace(tzinfo=None):
      raise serializers.ValidationError(f'End time :{value} should be a future time')
    return value

  def validate(self, data):
    start_time = data['start_time']
    end_time = data['end_time']
    if end_time < start_time:
      raise serializers.ValidationError(f'End Time can not be before than Start Time')

    # Check if session address belongs to user or not
    patient_id = data['patient']
    address_id = data['address']
    patient_address = Address.objects.filter(user_id__exact=patient_id).filter(id=address_id)
    if not patient_address:
      raise serializers.ValidationError(
        f'Address Id: {address_id} doesnt belong to patient Id: {patient_id}  ')
    # Check if appointment overlaps with another one
    overlapped_appointment = Appointment.objects.filter(
      start_time__range=[start_time, end_time]).first()
    if not overlapped_appointment is None:
      raise serializers.ValidationError(
        f'Requested appointment is overlapping with following appointment time {overlapped_appointment.id}'
      )
    overlapped_appointment = Appointment.objects.filter(
      end_time__range=[start_time, end_time]).first()
    if not overlapped_appointment is None:
      raise serializers.ValidationError(
        f'Requested appointment is overlapping with following appointment time {overlapped_appointment.id}'
      )
    # todo Check if requested appointment in away day
    return data

  @transaction.atomic
  def create(self, validated_data):
    patient = Patient.objects.get(user_id=validated_data.pop("patient"))
    therapist = Therapist.objects.get(user_id=validated_data.pop("therapist"))
    print('checking addresss')
    address = Address.objects.get(id=validated_data.pop("address"))
    appointment = Appointment.objects.create(patient=patient,
                                             therapist=therapist,
                                             address=address,
                                             **validated_data)
    return appointment
    # return Appointment(address=address, **validated_data).save()

  @transaction.atomic
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
    if not dec(value) <= Decimal(0.00) and dec(value) >= Decimal(5.001):
      raise serializers.ValidationError(f'rating: {value} should be between 0.0 and 5.0')
    return value

  @transaction.atomic
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
    rating_service = Rating(Rating.Type.CREATE)
    rating_service.calculate(therapist=appointment.therapist, new=validated_data.get('rating'))
    return review

  @transaction.atomic
  def update(self, instance, validated_data):
    try:
      appointment_id = validated_data.pop("appointment_id")
      appointment = Appointment.objects.get(pk=appointment_id)
    except Appointment.DoesNotExist:
      raise AppointmentNotFound(appointment_id)
    old_rating = instance.rating
    new_rating = validated_data.get('rating')
    if old_rating != new_rating:
      rating_service = Rating(Rating.Type.UPDATE)
      rating_service.calculate(therapist=appointment.therapist, new=new_rating, old=old_rating)
      instance.rating = new_rating

    instance.comment = validated_data.get('comment', instance.comment)
    instance.save()
    return instance


def dec(db_value):
  getcontext().prec = 2
  return Decimal(str(db_value))


class Rating:
  def __init__(self, rating_type):
    print(f'defining rating_type mk {rating_type}')
    self.rating_type = rating_type

  class Type(Enum):
    CREATE = 'CREATE'
    UPDATE = 'UPDATE'
    DELETE = 'DELETE'

  def calculate(self, therapist, new=None, old=None):
    average = therapist.rating
    nb_review = therapist.review_count
    if self.rating_type.value == self.Type.CREATE.value:
      therapist.rating = (dec(average) * nb_review + dec(new)) / (nb_review + 1)
      therapist.review_count = nb_review + 1
    elif self.rating_type.value == self.Type.UPDATE.value:
      therapist.rating = (dec(average) * nb_review - dec(old) + dec(new)) / nb_review
      therapist.review_count = nb_review
    elif self.rating_type.value == self.Type.DELETE.value:
      if nb_review > 1:
        therapist.rating = (dec(average) * nb_review - dec(old)) / (nb_review - 1)
        therapist.review_count = nb_review - 1
      else:
        therapist.rating = 0
        therapist.review_count = 0
    therapist.save()
