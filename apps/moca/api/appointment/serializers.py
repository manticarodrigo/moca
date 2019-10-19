from datetime import datetime
from django.db import models, transaction
from rest_framework import serializers
from rest_framework.exceptions import APIException
from decimal import *
from moca.api.appointment.errors import AppointmentAlreadyReviewed
from moca.api.appointment.errors import AppointmentNotFound
from moca.api.user.serializers import PatientSerializer, TherapistSerializer, UserSnippetSerializer
from moca.api.address.serializers import AddressSerializer
from moca.models import Address, User
from moca.models.appointment import Appointment, Review
from moca.models.user import Patient, Therapist, PATIENT_TYPE, THERAPIST_TYPE
from enum import *

from moca.api.util.Validator import RequestValidator


class AppointmentSerializer(serializers.ModelSerializer):
  address = AddressSerializer()
  other_party = serializers.SerializerMethodField()

  class Meta:
    model = Appointment
    fields = ['start_time', 'end_time', 'price', 'other_party', 'address']

  def get_other_party(self, obj):
    user_type = self.context['request'].user.type 
    if user_type not in (PATIENT_TYPE, THERAPIST_TYPE):
      raise APIException('Unsupported user type')

    if user_type == PATIENT_TYPE:
      party_user = obj.patient.user
    else: 
      party_user = obj.therapist.user

    return UserSnippetSerializer(party_user).data
    


class AppointmentCreateUpdateSerializer(serializers.ModelSerializer):
  address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())
  patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())

  class Meta:
    model = Appointment
    exclude = ['therapist']
    
  def create(self, validated_data):
    request = self.context['request']
    user = request.user
    therapist = Therapist.objects.get(user=user)

    validated_data['therapist'] = therapist
    appointment = Appointment.objects.create(**validated_data)
    return appointment


  def validate(self, data, **args):
    request = self.context['request']
    user = request.user
    instance = self.instance

    try:
      Therapist.objects.get(user=user)
    except:
      raise serializers.ValidationError(f'Appointment creator must be a therapist')

    start_time = data.get('start_time', instance.start_time)
    end_time = data.get('end_time', instance.end_time)

    if 'address' in data:
      address_id = data['address'].id
    else:
      address_id = instance.address_id

    if 'patient' in data:
      patient_id = data['patient'].user.id
    else:
      patient_id = instance.patient_id

    RequestValidator.future_time(start_time)
    RequestValidator.end_after_start(end_time, start_time)
    RequestValidator.address_belongs_to_user(address_id, patient_id)

    return data







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
      appointment_id = validated_data.pop('appointment_id')
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
      appointment_id = validated_data.pop('appointment_id')
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
