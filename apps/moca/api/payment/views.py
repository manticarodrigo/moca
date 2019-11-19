from rest_framework import permissions, generics
from moca.models.payment import Payment

from .permissions import IsOwner
from .serializers import PaymentSerializer


class PaymentListCreateView(generics.ListCreateAPIView):
  serializer_class = PaymentSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    return Payment.objects.filter(user=self.request.user)


class PaymentDetailView(generics.RetrieveUpdateDestroyAPIView):
  permission_classes = [IsOwner]
  lookup_url_kwarg = 'payment_id'
  queryset = Payment.objects.all()
  serializer_class = PaymentSerializer
