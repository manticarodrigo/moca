from rest_framework import generics

from moca.models.address import Address
from .serializers import AddressSerializer


class AddressCreateView(generics.CreateAPIView):
  serializer_class = AddressSerializer


class AddressDetailView(generics.RetrieveUpdateAPIView):
  lookup_url_kwarg = 'address_id'
  queryset = Address.objects.all()
  serializer_class = AddressSerializer
