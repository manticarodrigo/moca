from django.urls import path

from .views import ChatAPI, MessagesAPI

urlpatterns = [
  path('', ChatAPI.as_view()),  # get/post new chats
  path('<int:convid>/messages', MessagesAPI.as_view())
]
