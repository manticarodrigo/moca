from rest_framework import permissions
from rest_framework.generics import (CreateAPIView, RetrieveAPIView, UpdateAPIView)

from moca.models import User

from .serializers import UserSerializer


class UserAPIView(RetrieveAPIView, CreateAPIView, UpdateAPIView):
  permission_classes = [
    permissions.IsAuthenticated,
  ]

  queryset = User.objects.all()

  serializer_class = UserSerializer
