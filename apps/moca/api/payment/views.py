from rest_framework import permissions, generics, status
from rest_framework.response import Response

from .permissions import IsOwner
from .serializers import PaymentSerializer, PaymentSerializer
from moca.models.payment import Payment, PaymentProfile


class PaymentListCreateView(generics.ListCreateAPIView):
  serializer_class = PaymentSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    return Payment.objects.filter(user=self.request.user)


class PaymentDetailView(generics.DestroyAPIView):
  permission_classes = [IsOwner]
  lookup_url_kwarg = 'payment_id'
  queryset = Payment.objects.all()
  serializer_class = PaymentSerializer
