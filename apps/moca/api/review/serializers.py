from django.db import models

from rest_framework import serializers

from moca.api.user.serializers import UserSnippetSerializer
from moca.models.appointment import Review
from moca.models.user import User


class ReviewSerializer(serializers.ModelSerializer):

  class Meta:
    model = Review
    fields = ['comment', 'rating', 'patient']

  def to_representation(self, obj):
    representation = super().to_representation(obj)

    patient_id = representation['patient']
    patient = User.objects.get(id=patient_id)

    representation['patient'] = UserSnippetSerializer(patient).data

    return representation
