from django.db import models

from moca.models.user import Therapist


class Certification(models.Model):
  therapist = models.ForeignKey(Therapist, on_delete=models.CASCADE, related_name='certifications')
  title = models.CharField(max_length=50)
  description = models.TextField()

  def __str__(self):
    user = self.therapist.user
    return f'Therapist: {user.first_name} {user.last_name} \
             Title: {self.title} \
             Description: {self.description} \
            '


class CertificationImage(models.Model):
  certification = models.ForeignKey(Certification, on_delete=models.CASCADE, related_name="images")
  image = models.ImageField(upload_to='certifications',)

  def __str__(self):
    user = self.certification.therapist.user
    return f'Therapist: {user.first_name} {user.last_name} \
             Certification ID: {self.certification.id} \
             Image ID: {self.image.id} \
            '
