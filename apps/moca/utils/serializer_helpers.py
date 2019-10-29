import functools

from django.contrib.auth.models import User
from django.db import transaction
from drf_yasg.utils import swagger_serializer_method
from rest_framework import serializers
from rest_framework.exceptions import APIException
from rest_framework.utils.serializer_helpers import BindingDict

serializer_id = 0


def get_default_name(serA, serB):
  global serializer_id
  serializer_id = serializer_id + 1
  return f'Serializer{serializer_id}'

def combineSerializers(SerAClass, SerBClass, serializerName=get_default_name):
  serA = SerAClass()
  serB = SerBClass()

  fieldsA = set(serA.fields)
  fieldsB = set(serB.fields)

  def valueFor(soFar, field):
    (fieldA, fieldB) = (field, None) if field in fieldsA else (None, field)

    if fieldA:
      soFar.append((fieldA, serA.get_fields()[fieldA]))
    elif fieldB:
      soFar.append((fieldB, serB.get_fields()[fieldB]))

    return soFar

  class NewSerializer(serializers.Serializer):
    @property
    def fields(self):
      fields = functools.reduce(valueFor, sorted(fieldsA.union(fieldsB)), [])
      self._fields = dict(fields)
      return self._fields

  NewSerializer.__name__ = serializerName(serA, serB)

  return NewSerializer
