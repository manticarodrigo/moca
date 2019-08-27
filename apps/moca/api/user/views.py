from django.db import transaction
from rest_framework import generics, permissions, serializers
from rest_framework.response import Response
from moca.models import User, Address
from .serializers import UserSerializer


class UserAPIView(generics.RetrieveAPIView):
  permission_classes = [
    permissions.IsAuthenticated,
  ]

  serializer_class = UserSerializer

  @transaction.atomic
  def post(self, request):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    serializer.save()

    return Response(serializer.data)
