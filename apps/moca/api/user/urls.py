from django.contrib import admin
from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (PatientCreateView, PatientDetailView, TherapistCreateView, TherapistDetailView,
                    TherapistSearchView, TherapistLeaveView, TherapistLeaveDetailView,
                    TherapistPricingListCreateView, verify_email,
                    TherapistCertificationListCreateView, TherapistCertificationDetailView,
                    TherapistPricingDetailView)

urlpatterns = [
  path('verify/<str:token>', verify_email),
  # patient
  path('patient/', PatientCreateView.as_view(), name='create-patient'),
  path('patient/<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
  # therapist
  path('therapist/', TherapistCreateView.as_view(), name='create-therapist'),
  path('therapist/<int:pk>/', TherapistDetailView.as_view(), name='therapist-detail'),
  path('therapist/prices/', TherapistPricingListCreateView.as_view(), name='therapist-prices'),
  path('therapist/prices/<int:price_id>',
       TherapistPricingDetailView.as_view(),
       name='therapist-price-details'),
  path('therapist/certifications/',
       TherapistCertificationListCreateView.as_view(),
       name='therapist-cert'),
  path('therapist/certifications/<int:certification_id>',
       TherapistCertificationDetailView.as_view(),
       name='therapist-cert-detail'),
  path('therapist/search/', TherapistSearchView.as_view(), name='therapist-search'),
  path('therapist/away/', TherapistLeaveView.as_view(), name='therapist-away'),
  path('therapist/away/<int:leave_id>',
       TherapistLeaveDetailView.as_view(),
       name='therapist-away-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
