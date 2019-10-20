from datetime import datetime
from django.db import models, transaction
from rest_framework import serializers
from rest_framework.exceptions import APIException
from django.db.models import ForeignKey
from decimal import *
from moca.api.appointment.errors import AppointmentAlreadyReviewed
from moca.api.appointment.errors import AppointmentNotFound
from moca.api.user.serializers import PatientSerializer, TherapistSerializer, UserSnippetSerializer
from moca.api.address.serializers import AddressSerializer
from moca.models import Address, User
from moca.models.appointment import Appointment, Review
from moca.models.user import Patient, Therapist

from moca.api.util.Validator import RequestValidator


class ReviewSerializer(serializers.ModelSerializer):
  class Meta:
    model = Review
    fields = ['comment', 'rating']


class AppointmentSerializer(serializers.ModelSerializer):
  address = AddressSerializer()
  other_party = serializers.SerializerMethodField()
  review = ReviewSerializer()

  class Meta:
    model = Appointment
    fields = ['id', 'start_time', 'end_time', 'price', 'other_party', 'address', 'review']

  def get_other_party(self, obj):
    user_type = self.context['request'].user.type 
    if user_type not in (User.PATIENT_TYPE, User.THERAPIST_TYPE):
      raise APIException('Unsupported user type')

    if user_type == User.PATIENT_TYPE:
      party_user = obj.patient.user
    else: 
      party_user = obj.therapist.user

    return UserSnippetSerializer(party_user).data


class AppointmentCreateUpdateSerializer(serializers.ModelSerializer):
  address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())
  patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
  review = ReviewSerializer(required=False)

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

  def update(self, instance, validated_data):
    if 'review' in validated_data:
      review_data = validated_data.pop('review')
      try:
        review = instance.review
      except:
        review = Review(appointment=instance, therapist_id=instance.therapist_id)

      review.rating = review_data.get('rating', review.rating)
      review.comment = review_data.get('comment', review.comment)
      review.save()
      Therapist.objects.get(pk=instance.therapist_id).update_rating()

    return super(AppointmentCreateUpdateSerializer, self).update(instance, validated_data)


  def validate(self, data):
    request = self.context['request']
    user = request.user
    instance = self.instance

    def _get_require_field(name, data, instance):
      model_field = self.Meta.model._meta.get_field(name)
      is_foreign_key = isinstance(model_field, ForeignKey)
      return_value = None

      if is_foreign_key:
        if name in data:
            return_value = data[name].id
        elif name+"_id" in instance.__dict__:
          return_value = getattr(instance, name+"_id")
      else:
        if name in data:
            return_value = data[name]
        elif name in instance.__dict__:
          return_value = getattr(instance, name)
      
      if not return_value:
        raise serializers.ValidationError(f"{name} is required")
      
      return return_value

    try:
      Therapist.objects.get(user=user)
    except:
      raise serializers.ValidationError(f'Appointment creator must be a therapist')

    start_time = _get_require_field('start_time', data, instance)
    end_time = _get_require_field('end_time', data, instance)
    address_id = _get_require_field('address', data, instance)

    if 'patient' in data:
      patient_id = data['patient'].user.id
    else:
      patient_id = instance.patient_id

    RequestValidator.future_time(start_time)
    RequestValidator.end_after_start(end_time, start_time)
    RequestValidator.address_belongs_to_user(address_id, patient_id)

    return data
