from django.db import models
from django.conf import settings
from django.contrib.gis.db import models as gisModels


class AddressManager(models.Manager):

    def create_user_addresses(self, user) -> []:
        saved_addresses = []
        if 'addresses' in user:
            addresses = user.pop('addresses', default=[])
            for address in addresses:
                address = Address.objects.create(user=user, **address)
                saved_addresses.add(address)
        return saved_addresses


class Address(models.Model):
    # Address label
    name = models.CharField(max_length=50)
    # Actual adress
    text = models.CharField(max_length=300)
    primary = models.BooleanField()
    apartment = models.CharField(max_length=50)
    location = gisModels.PointField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             related_name="addresses",
                             on_delete=models.CASCADE)

    objects = AddressManager()

    def __str__(self):
        return f"name: {self.name},text: {self.text}, " \
               f"primary:{self.primary},location:{self.location}" \
               + self.location

    # street = models.CharField(max_length=50)
    # zip_code = models.SmallIntegerField()
    # city = models.CharField(max_length=50)
    # state = models.CharField(max_length=2)
