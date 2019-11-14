from knox.models import AuthToken
from rest_framework import generics
from rest_framework.response import Response
from moca.models.user import Device

from moca.api.user.serializers import UserSerializer

from .serializers import LoginSerializer


class LoginAPIView(generics.GenericAPIView):
  permission_classes = []
  serializer_class = LoginSerializer

  def post(self, request, *args, **kwargs):
    device_token = request.data.pop('device_token', None)
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data
    auth_token = AuthToken.objects.create(user)

    if device_token:
      Device.objects.update_or_create(
        user=user,
        token=device_token,
      )
    return Response({**UserSerializer(user).data, "token": auth_token[1]})
