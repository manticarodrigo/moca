from rest_framework import permissions, generics

from moca.models.address import Address
from .serializers import AddressSerializer, AddressCreateSerializer

# POST {{ENV}}/api/user/address
class AddressCreateView(generics.CreateAPIView):
  serializer_class = AddressCreateSerializer
  permission_classes = [permissions.IsAuthenticated]

# GET {{ENV}}/api/user/address/{id}
class AddressDetailView(generics.RetrieveUpdateAPIView):
  serializer_class = AddressSerializer
  permission_classes = [permissions.IsAuthenticated]
