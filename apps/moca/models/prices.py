from django.db import models

from moca.models.user import Therapist


class Price(models.Model):
  SESSION_TYPES = [('thirty', 'Thirty minutes'), ('fourtyfive', 'Fourty five minutes'),
                   ('sixty', 'Sixty minutes'), ('evaluation', 'Evaluation')]

  therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name="prices")
  session_type = models.CharField(max_length=20, choices=SESSION_TYPES)
  price = models.PositiveIntegerField()

  class Meta:
    unique_together = ('therapist', 'session_type',)
