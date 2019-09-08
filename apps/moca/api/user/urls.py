from django.contrib import admin
from django.urls import include, path
from .views import UserAPIDetail, UserAPIView, UserDeviceView\
    # , UserDeviceDetail
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # post, get(for search)
    path('', UserAPIView.as_view()),
    # get(retrieve by id), put
    path('<int:user_id>/', UserAPIDetail.as_view()),
    # post, get(for search)
    path('devices/', UserDeviceView.as_view()),
    # path('devices/<int:device_id>/', UserDeviceDetail.as_view())
]
urlpatterns = format_suffix_patterns(urlpatterns)
