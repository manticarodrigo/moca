from rest_framework import generics

from moca.models.address import Address
from .serializers import AddressSerializer
from rest_framework.exceptions import APIException


class AddressCreateView(generics.CreateAPIView):
  serializer_class = AddressSerializer


class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
  lookup_url_kwarg = 'address_id'
  queryset = Address.objects.all()
  serializer_class = AddressSerializer

  def delete(self, request, *args, **kwargs):
    address_id = kwargs.get("address_id")
    try:
      to_delete = Address.objects.get(id=address_id)
    except:
      return self.destroy(request, *args, **kwargs)

    count = Address.objects.filter(user=request.user).count()

    if count == 1:
      raise APIException('Can not delete last address')

    if to_delete.primary:
      raise APIException('Can not delete primary address')

    return self.destroy(request, *args, **kwargs)
