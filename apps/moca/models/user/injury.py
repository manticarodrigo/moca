from django.db import models

from moca.models.user import Patient


class Injury(models.Model):
  patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name="injuries")
  title = models.CharField(max_length=50)
  description = models.TextField()

  def __str__(self):
    return f'Patient: {self.patient.user.first_name} Injury ID: {self.id}'


class InjuryImage(models.Model):
  injury = models.ForeignKey(Injury, on_delete=models.CASCADE, related_name="images")
  image = models.ImageField(upload_to='injuries',)

  def __str__(self):
    return f'Patient: {self.injury.patient.user.first_name} Injury ID: {self.injury.id}'
