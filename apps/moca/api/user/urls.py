from django.contrib import admin
from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (PatientCreateView, PatientDetailView, TherapistCreateView, TherapistDetailView,
                    TherapistSearchView, TherapistLeaveView, TherapistLeaveDetailView,
                    TherapistPricingListCreateView, verify_email, TherapistCertificationListCreateView,
                    TherapistCertificationDetailView, TherapistPricingDetailView)

urlpatterns = [
  path('verify/<str:token>', verify_email),
  # patient
  path('patient/', PatientCreateView.as_view()),
  path('patient/<int:pk>/', PatientDetailView.as_view()),
  # therapist
  path('therapist/', TherapistCreateView.as_view()),
  path('therapist/<int:pk>/', TherapistDetailView.as_view()),
  path('therapist/prices/', TherapistPricingListCreateView.as_view()),
  path('therapist/prices/<int:price_id>', TherapistPricingDetailView.as_view()),
  path('therapist/certifications/', TherapistCertificationListCreateView.as_view()),
  path('therapist/certifications/<int:certification_id>', TherapistCertificationDetailView.as_view()),
  path('therapist/search/', TherapistSearchView.as_view()),
  path('therapist/away/', TherapistLeaveView.as_view()),
  path('therapist/away/<int:leave_id>', TherapistLeaveDetailView.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
