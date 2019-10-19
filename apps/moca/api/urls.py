from django.contrib import admin
from django.urls import path, include


urlpatterns = [
  path('chat/', include('moca.api.chat.urls')),
  path('user/', include('moca.api.user.urls')),
  path('authenticate/', include('moca.api.authenticate.urls')),
  path('appointment/', include('moca.api.appointment.urls')),
  path('device/', include('moca.api.device.urls')),
  path('address/', include('moca.api.address.urls')),
  path('payment/', include('moca.api.payment.urls')),
]
