from knox.models import AuthToken
from rest_framework import generics, permissions
from rest_framework.response import Response

from moca.api.user.serializers import PatientSerializer

from .serializers import LoginSerializer


class RegisterAPIView(generics.GenericAPIView):
  serializer_class = PatientSerializer


class LoginAPIView(generics.GenericAPIView):
  serializer_class = LoginSerializer

  def post(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data
    return Response({
      "user": PatientSerializer(user, context=self.get_serializer_context()).data,
      "token": AuthToken.objects.create(user)[1]
    })
