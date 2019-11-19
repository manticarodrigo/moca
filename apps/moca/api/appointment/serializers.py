from datetime import datetime
from django.db import models, transaction
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework.exceptions import APIException
from django.db.models import ForeignKey

from moca.api.user.serializers import PatientSerializer, TherapistSerializer, UserSnippetSerializer
from moca.api.address.serializers import AddressSerializer
from moca.models import Address, User
from moca.models.appointment import Appointment, AppointmentRequest, Review, Note, NoteImage
from moca.models.user import Patient, Therapist
from moca.api.util.Validator import RequestValidator


class AppointmentReviewSerializer(serializers.ModelSerializer):
  class Meta:
    model = Review
    fields = ['comment', 'rating']

class NoteImageSerializer(serializers.ModelSerializer):
  class Meta:
    model = NoteImage
    fields = ['id', 'image']

class NoteSerializer(serializers.ModelSerializer):
  images = NoteImageSerializer(many=True, read_only=True)

  class Meta:
    model = Note
    fields = ['subjective', 'objective', 'treatment', 'assessment', 'diagnosis', 'images']

  def update(self, instance, validated_data):
    images_data = self.context.get('view').request.FILES

    for image_data in images_data.getlist('images'):
      NoteImage.objects.create(note=instance, image=image_data)

    return super(NoteSerializer, self).update(instance, validated_data)


class AppointmentSerializer(serializers.ModelSerializer):
  address = AddressSerializer()
  therapist_rating = serializers.SerializerMethodField()
  other_party = serializers.SerializerMethodField()
  review = AppointmentReviewSerializer(required=False)
  note = NoteSerializer(read_only=True)

  class Meta:
    model = Appointment
    fields = [
      'id', 'start_time', 'end_time', 'price', 'other_party', 'address', 'review', 'note',
      'status', 'therapist_rating'
    ]

  def get_therapist_rating(self, appointment):
    return appointment.therapist.rating

  @swagger_serializer_method(serializer_or_field=UserSnippetSerializer)
  def get_other_party(self, obj):
    user_type = self.context['request'].user.type
    if user_type not in (User.PATIENT_TYPE, User.THERAPIST_TYPE):
      raise APIException('Unsupported user type')

    if user_type == User.PATIENT_TYPE:
      party_user = obj.therapist.user
    else:
      party_user = obj.patient.user

    return UserSnippetSerializer(party_user).data


class AppointmentRequestSerializer(serializers.ModelSerializer):
  address = AddressSerializer()

  class Meta:
    model = AppointmentRequest
    fields = ['id', 'start_time', 'end_time', 'price', 'status', 'address']


class AppointmentRequestCreateSerializer(serializers.ModelSerializer):
  address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())
  patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
  therapist = serializers.PrimaryKeyRelatedField(queryset=Therapist.objects.all())

  class Meta:
    model = AppointmentRequest
    fields = '__all__'

  def validate(self, data):
    instance = self.instance
    request = self.context['request']
    user = request.user

    try:
      Therapist.objects.get(user=user)
    except:
      raise serializers.ValidationError(f'Appointment creator must be a therapist')

    start_time = data.get('start_time')
    end_time = data.get('end_time')
    address_id = data.get('address').id
    patient_id = data.get('patient').user.id

    RequestValidator.future_time(start_time)
    RequestValidator.end_after_start(end_time, start_time)
    RequestValidator.address_belongs_to_user(address_id, patient_id)

    return data


class AppointmentCreateUpdateSerializer(serializers.ModelSerializer):
  address = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all())
  patient = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all())
  therapist = serializers.PrimaryKeyRelatedField(queryset=Therapist.objects.all())
  review = AppointmentReviewSerializer(required=False)
  note = NoteSerializer(required=False)

  class Meta:
    model = Appointment
    fields = '__all__'

  def update(self, instance, validated_data):
    request = self.context['request']
    user = request.user

    if 'review' in validated_data:
      review_data = validated_data.pop('review')

      def update_review(review):
        review.rating = review_data.get('rating', review.rating)
        review.comment = review_data.get('comment', review.comment)
        review.save()
        Therapist.objects.get(pk=instance.therapist_id).update_rating()

      if user.type == User.PATIENT_TYPE:
        try:
          review = instance.review
          update_review(review)
        except:
          review = Review(appointment=instance,
                          therapist_id=instance.therapist_id,
                          patient_id=user.id)
          update_review(review)

    return super(AppointmentCreateUpdateSerializer, self).update(instance, validated_data)

  def create(self, validated_data):
    patient_id = validated_data['patient'].user_id
    try:
      primary_address = Address.objects.get(user_id=patient_id, primary=True)
    except:
      raise APIException('Patient does not have a primary address')

    validated_data['address'] = primary_address
    return super(AppointmentCreateUpdateSerializer, self).create(validated_data)

  # TODO check which fields can be updates and their validations
  def validate(self, data):
    return data
