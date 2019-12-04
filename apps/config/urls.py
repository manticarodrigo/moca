"""moca URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
from django.urls import path, re_path, include
from django.views.generic import TemplateView

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
  openapi.Info(
    title="MOCA API",
    default_version='v1',
  ),
  public=True,
  # TODO: Secure access to docs for admins only
  permission_classes=(permissions.AllowAny, ),
)

urlpatterns = [
  path('admin/', admin.site.urls),
  path('api/', include('moca.api.urls')),
  path('api/docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
  path('api/docs/swagger.yaml', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

if settings.DEBUG:
  from django.contrib.staticfiles.urls import staticfiles_urlpatterns
  from django.conf.urls.static import static

  urlpatterns += staticfiles_urlpatterns()
  urlpatterns += static('media', document_root=settings.MEDIA_ROOT)