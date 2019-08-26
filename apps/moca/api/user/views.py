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

  def get(self, request):
    return Response({})

  @transaction.atomic
  def post(self, request):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    validated = serializer.validated_data

    user = User.objects.create_user(first_name=validated['first_name'],
                                    last_name=validated['last_name'],
                                    gender=validated['gender'],
                                    date_of_birth=validated['date_of_birth'],
                                    type=validated['type'],
                                    email=validated['email'])

    user.save()

    addresses = [
      Address.objects.create(name=address['name'],
                             text=address['text'],
                             location=address['location'],
                             primary=address['primary'],
                             user=user) for address in validated['addresses']
    ]

    for address in addresses:
      address.save()

    return Response(serializer.data)
