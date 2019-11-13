from .serializers import AddressSerializer
from rest_framework.exceptions import APIException
from rest_framework import generics, status
from rest_framework.response import Response

from moca.models.address import Address


class AddressCreateView(generics.CreateAPIView):
  serializer_class = AddressSerializer


class AddressDetailView(generics.RetrieveUpdateDestroyAPIView):
  lookup_url_kwarg = 'address_id'
  queryset = Address.objects.all()
  serializer_class = AddressSerializer

  def delete(self, request, *args, **kwargs):
    address_id = kwargs.get("address_id")
    try:
      to_delete = Address.objects.get(id=address_id, archive=False)
    except:
      raise APIException('No such address')

    count = Address.objects.filter(user=request.user, archive=False).count()

    if count == 1:
      raise APIException('Can not delete last address.')

    if to_delete.primary:
      raise APIException('Can not delete active address.')

    to_delete.archive = True
    to_delete.save()

    return Response(status=status.HTTP_200_OK)
