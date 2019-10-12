from django.conf import settings
from django.contrib.gis.db import models as gisModels
from django.db import models


class Address(models.Model):
  # Address label
  name = models.CharField(max_length=50)
  # Address fields
  street = models.CharField(max_length=50)
  apartment = models.CharField(max_length=50)
  zip_code = models.CharField(max_length=5)
  city = models.CharField(max_length=50)
  state = models.CharField(max_length=2)
  # Actual coordinates
  primary = models.BooleanField()
  location = gisModels.PointField()
  user = models.ForeignKey(settings.AUTH_USER_MODEL,
                           related_name="addresses",
                           on_delete=models.CASCADE,
                           blank=True,
                           null=True)


  def __str__(self):
    return f"name: {self.name},text: {self.street}, " \
           f"primary:{self.primary},location:{self.location}" \
           f" user:{self.user}"
