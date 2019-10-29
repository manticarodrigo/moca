from django.urls import path

from .views import ConversationListView, MessageListCreateView

urlpatterns = [
  path('', ConversationListView.as_view(), name='get-chats'),
  path('<int:user_id>/', MessageListCreateView.as_view(), name='send-message'),
]
