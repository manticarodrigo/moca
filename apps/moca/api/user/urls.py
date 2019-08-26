from django.contrib import admin
from django.urls import path, include
from .views import UserAPIView

urlpatterns = [
  path('', UserAPIView.as_view()),
]
