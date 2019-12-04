from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (connect_login_url, connect_oauth_callback, PaymentListCreateView,
                    PaymentDetailView)

urlpatterns = [
  # connected accounts oauth
  path('connect/login/', connect_login_url, name='payment-connect-login'),
  path('connect/callback/', connect_oauth_callback, name='payment-connect-callback'),
  # payment info
  path('', PaymentListCreateView.as_view()),
  path('<int:payment_id>', PaymentDetailView.as_view(), name='payment-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
