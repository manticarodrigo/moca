from django.urls import path

from .views import DeviceAPIView

urlpatterns = [
  path('add/', DeviceAPIView.as_view()),
]
