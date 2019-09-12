from django.contrib import admin
from django.urls import include, path
from .views import PatientAPIDetail, PatientAPIView, UserDeviceView\
    # , UserDeviceDetail
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    # post, get(for search)
    path('patient/', PatientAPIView.as_view()),
    # get(retrieve by id), put
    path('patient/<int:user_id>/', PatientAPIDetail.as_view()),
    # post, get(for search)
    path('therapist/', PatientAPIView.as_view()),
    # get(retrieve by id), put
    path('therapist/<int:user_id>/', PatientAPIDetail.as_view()),
    # post, get(for search)
    path('devices/', UserDeviceView.as_view()),
    # path('devices/<int:device_id>/', UserDeviceDetail.as_view())
]
urlpatterns = format_suffix_patterns(urlpatterns)
