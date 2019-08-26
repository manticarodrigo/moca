from django.contrib import admin
from django.urls import path, include
from .views import ConversationView, ConversationListView

urlpatterns = [
  path('', ConversationListView.as_view()),
  path('<int:id>/', ConversationView.as_view())
]
