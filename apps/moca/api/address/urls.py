from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import AddressCreateView, AddressDetailView

urlpatterns = [
  path('', AddressCreateView.as_view(), name='create-address'),
  path('<int:address_id>', AddressDetailView.as_view(), name='address-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
