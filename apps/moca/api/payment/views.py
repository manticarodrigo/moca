from rest_framework import permissions, generics

from .serializers import PaymentSerializer, PaymentSerializer
from moca.models.payment import Payment


class PaymentListCreateView(generics.ListCreateAPIView):
  serializer_class = PaymentSerializer
  permission_classes = [permissions.IsAuthenticated]
  pagination_class = None

  def get_queryset(self):
    return Payment.objects.filter(user=self.request.user)
