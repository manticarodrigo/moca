from rest_framework import generics

from .serializers import DeviceSerializer

class DeviceAPIView(generics.CreateAPIView):
  serializer_class = DeviceSerializer
