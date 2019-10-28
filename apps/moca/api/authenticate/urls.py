from django.urls import path
from knox.views import LogoutView

from .views import LoginAPIView

urlpatterns = [
  path("login", LoginAPIView.as_view(), name='knox_login'),
  path('logout', LogoutView.as_view(), name='knox_logout')
]
