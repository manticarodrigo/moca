from django.contrib import admin
from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (PatientAPIDetail, PatientAPIView, TherapistAPIDetailView, TherapistAPIView,
                    TherapistLeaveAPIView, TherapistLeaveDetailView,
                    TherapistPricing)

urlpatterns = [
  # post, get(for search)
  path('patient/', PatientAPIView.as_view()),
  # get(retrieve by id), put
  path('patient/<int:patient_id>/', PatientAPIDetail.as_view()),
  # post, get(for search)
  path('therapist/', TherapistAPIView.as_view()),
  # get(retrieve by id), put
  path('therapist/<int:therapist_id>/', TherapistAPIDetailView.as_view()),
  path('therapist/<int:therapist_id>/tariffs', TherapistPricing.as_view()),
  # away
  path('therapist/away/', TherapistLeaveAPIView.as_view()),
  path('therapist/away/<int:leave_id>', TherapistLeaveDetailView.as_view())
]
urlpatterns = format_suffix_patterns(urlpatterns)
