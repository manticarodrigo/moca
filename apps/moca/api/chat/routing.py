from django.urls import path

from . import messaging

websocket_urlpatterns = [
    path('ws/chat/<slug:room_name>/', messaging.ChatConsumer),
]