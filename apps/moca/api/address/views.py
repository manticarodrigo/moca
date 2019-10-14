from rest_framework import permissions, generics

from .serializers import AddressSerializer

# POST {{ENV}}/api/user/address
class AddressCreateView(generics.CreateAPIView):
  serializer_class = AddressSerializer
  permission_classes = [permissions.IsAuthenticated]
