from django.urls import path

# from .views import ChatAPI, MessagesAPI
from .views import ConversationListView

urlpatterns = [
  # get all conversations
  path('', ConversationListView.as_view()),  # get/post new chats
  # send a message to a user or get all messages from a user
  # path('<int:user_id>/', ConversationListView.as_view()),  # get/post new chats

  # path('<int:user_id>/messages', MessagesAPI.as_view())
]
