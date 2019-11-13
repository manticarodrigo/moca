from knox.models import AuthToken
from rest_framework import generics
from rest_framework.response import Response

from moca.api.user.serializers import UserSerializer

from .serializers import LoginSerializer


class LoginAPIView(generics.GenericAPIView):
  permission_classes = []
  serializer_class = LoginSerializer

  def get_serializer_context(self):
    context = super().get_serializer_context()
    context['my_value'] = "hello"
    return context

  def post(self, request, *args, **kwargs):
  
    serializer = self.get_serializer(data=request.data)
    # print("CONT", request.context)
    serializer.is_valid(raise_exception=True)
    user = serializer.validated_data
    return Response({**UserSerializer(user).data, "token": AuthToken.objects.create(user)[1]})
