from django.contrib import admin
from django.urls import include, path

from .views import UserAPIView

urlpatterns = [
  # post, get(for search)
  path('', UserAPIView.as_view()),
  # put, get
  path('<int:pk>/', UserAPIView.as_view())
]
