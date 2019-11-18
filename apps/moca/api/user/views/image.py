from rest_framework import generics
from rest_framework.parsers import MultiPartParser

from moca.models import User

from ..permissions import IsUserSelf
from ..serializers import UserImageSerializer

class UserImageView(generics.UpdateAPIView):
  serializer_class = UserImageSerializer
  queryset = User.objects
  permission_classes = [IsUserSelf]
  parser_classes = (MultiPartParser,)
