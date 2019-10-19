from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import PaymentListCreateView

urlpatterns = [
  path('', PaymentListCreateView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
