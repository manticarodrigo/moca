from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import PaymentListCreateView, PaymentDetailView

urlpatterns = [
  path('', PaymentListCreateView.as_view()),
  path('<int:payment_id>', PaymentDetailView.as_view(), name='payment-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
