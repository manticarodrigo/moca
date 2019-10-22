from django.db import models

from moca.models.user import Therapist


class Price(models.Model):
  therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name="prices")
  session_type = models.CharField(max_length=20)
  price = models.PositiveIntegerField()

  class Meta:
    unique_together = ['therapist', 'session_type']
