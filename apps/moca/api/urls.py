
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
  path('chat/', include('moca.api.chat.urls')),
  path('user/', include('moca.api.user.urls')),
  path('authenticate/', include('moca.api.authenticate.urls')),
]  