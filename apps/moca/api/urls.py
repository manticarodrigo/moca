from django.contrib import admin
from django.urls import path, include
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
  openapi.Info(
    title="MOCA API",
    default_version='v1',
  ),
  public=False,
)

urlpatterns = [
  path('swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-json'),
  path('chat/', include('moca.api.chat.urls')),
  path('user/', include('moca.api.user.urls')),
  path('authenticate/', include('moca.api.authenticate.urls')),
  path('appointment/', include('moca.api.appointment.urls')),
  path('device/', include('moca.api.device.urls')),
]
