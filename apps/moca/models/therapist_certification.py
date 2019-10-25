from django.db import models

from moca.models.user import Therapist


class TherapistCertification(models.Model):
  therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name='certifications')
  title = models.CharField(max_length=50)
  image = models.ImageField(upload_to='certifications', null=True)