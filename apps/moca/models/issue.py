from django.db import models

from moca.models import Appointment
from moca.models.user import Therapist, Patient


class Issue(models.Model):
  PRIORITIES = [('high', 'high'), ('normal', 'normal'), ('low', 'low')]

  therapist = models.ForeignKey(Therapist, on_delete=models.DO_NOTHING, null=True)
  patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING, null=True)
  appointment = models.ForeignKey(Appointment, on_delete=models.DO_NOTHING, null=True)
  priority = models.CharField(max_length=20, choices=PRIORITIES, default="normal")
  description = models.TextField(null=True)
