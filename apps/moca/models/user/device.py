from django.db import models
from knox.models import AuthToken

from .user import User

class Device(models.Model):
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  token = models.CharField(max_length=50)
  auth_token = models.ForeignKey(AuthToken, on_delete=models.CASCADE)
