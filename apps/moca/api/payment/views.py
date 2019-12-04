from django.db import IntegrityError
from django.http import HttpResponseRedirect

from rest_framework import permissions, generics
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from moca.models import User, MerchantProfile, Payment
from moca.services.stripe import get_connect_oauth_url, get_connect_login_url, connect_account

from .permissions import IsOwner
from .serializers import PaymentSerializer



@api_view(['GET'])
def connect_login_url(request):
  try:
    merchant_id = MerchantProfile.objects.get(user=request.user).stripe_user_id
    return Response(get_connect_login_url(merchant_id))
  except MerchantProfile.DoesNotExist:
    return Response(get_connect_oauth_url(request.user))
    

@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def connect_oauth_callback(request):
  # TODO: need a non-naive authentication strategy for mobile apps
  user_id = request.query_params.get('state')
  code = request.query_params.get('code')

  user = User.objects.get(id=user_id)
  stripe_user_id = connect_account(code)

  if user.type != User.THERAPIST_TYPE:
    return Response('Only therapists are allowed to create connected accounts.')

  try:
    MerchantProfile.objects.create(user=user, stripe_user_id=stripe_user_id)
  except IntegrityError:
    return Response('Stripe account has already been to connected to MOCA.')

  return HttpResponseRedirect(get_connect_login_url(stripe_user_id))

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
