from django.db import models

from rest_framework import serializers
from drf_yasg.utils import swagger_serializer_method

from moca.api.user.serializers import UserSnippetSerializer
from moca.models.appointment import Review
from moca.models.user import User


class ReviewSerializer(serializers.ModelSerializer):
  patient = serializers.SerializerMethodField()

  class Meta:
    model = Review
    fields = ['id', 'comment', 'rating', 'patient']

  @swagger_serializer_method(serializer_or_field=UserSnippetSerializer)
  def get_patient(self, obj):
    return UserSnippetSerializer(obj.patient.user).data
