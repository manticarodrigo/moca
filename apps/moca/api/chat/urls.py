from django.urls import path

from .views import ConversationListView, MessageListCreateView

urlpatterns = [
  path('', ConversationListView.as_view()),
  path('<int:user_id>/', MessageListCreateView.as_view()),
]
