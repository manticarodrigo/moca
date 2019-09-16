from django.urls import path
from knox.views import LogoutView

from .views import LoginAPIView, RegisterAPIView

urlpatterns = [
  path("login", LoginAPIView.as_view()),
  path('logout', LogoutView.as_view(), name='knox_logout')
]
