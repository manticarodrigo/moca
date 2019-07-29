
from django.contrib import admin
from django.urls import path, include
from .views import Conversation, ConversationList

urlpatterns = [
  path('', ConversationList.as_view()),
  path('<int:id>/', Conversation.as_view())
]  