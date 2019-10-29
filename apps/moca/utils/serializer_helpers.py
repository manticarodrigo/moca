from django.contrib.auth.models import User
from django.db import transaction
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.utils.serializer_helpers import BindingDict

from moca.api.appointment.serializers import (AppointmentRequestCreateSerializer,
                                              AppointmentRequestSerializer)
from moca.api.user.serializers import UserSnippetSerializer
from moca.models import (Address, AppointmentRequest, AppointmentRequestMessage, Conversation,
                         ImageMessage, Message, TextMessage)
serializer_id = 0


def get_default_name(serA, serB):
  global serializer_id
  serializer_id = serializer_id + 1
  return f'Serializer{serializer_id}'


def combineSerializers(serA, serB, serializerName=get_default_name):
  class NewSerializer(serializers.Serializer):
    @property
    def fields(self):
      fieldsA = set(serA.Meta.fields)
      fieldsB = set(serB.Meta.fields)

      fields = []
      for field in fieldsA.union(fieldsB):
        real_field = None

        if field in fieldsA.intersection(fieldsB):
          real_field = serA().get_fields()[field]
        elif field in fieldsA:
          real_field = serA().get_fields()[field]
        elif field in fieldsB:
          real_field = serB().get_fields()[field]

        fields.append((field, real_field))

      self._fields = dict(fields)
      return self._fields

  NewSerializer.__name__ = serializerName(serA, serB)

  return NewSerializer
