from django.contrib import admin
from django.urls import include, path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import (verify_email, UserImageView, TherapistCreateView, TherapistDetailView,
                    TherapistCertificationCreateView, TherapistCertificationDetailView,
                    TherapistSearchView, TherapistAwayPeriodListCreateView,
                    TherapistAwayPeriodDetailView, TherapistPricingListCreateView,
                    TherapistPricingDetailView, PatientCreateView, PatientDetailView,
                    PatientInjuryCreateView, PatientInjuryDetailView)

urlpatterns = [
  path('verify/<str:token>', verify_email),
  path('<int:pk>/image/', UserImageView.as_view(), name='user-image'),
  # patient
  path('patient/', PatientCreateView.as_view(), name='create-patient'),
  path('patient/<int:pk>/', PatientDetailView.as_view(), name='patient-detail'),
  path('patient/injury/', PatientInjuryCreateView.as_view(), name='patient-injury'),
  path('patient/injury/<int:injury_id>/', PatientInjuryDetailView.as_view(), name='patient-injury-detail'),
  # therapist
  path('therapist/', TherapistCreateView.as_view(), name='create-therapist'),
  path('therapist/<int:pk>/', TherapistDetailView.as_view(), name='therapist-detail'),
  path('therapist/prices/', TherapistPricingListCreateView.as_view(), name='therapist-prices'),
  path('therapist/prices/<int:price_id>',
       TherapistPricingDetailView.as_view(),
       name='therapist-price-details'),
  path('therapist/certifications/',
       TherapistCertificationCreateView.as_view(),
       name='therapist-cert'),
  path('therapist/certifications/<int:certification_id>/',
       TherapistCertificationDetailView.as_view(),
       name='therapist-cert-detail'),
  path('therapist/search/', TherapistSearchView.as_view(), name='therapist-search'),
  path('therapist/away/', TherapistAwayPeriodListCreateView.as_view(), name='therapist-away'),
  path('therapist/away/<int:period_id>',
       TherapistAwayPeriodDetailView.as_view(),
       name='therapist-away-detail')
]

urlpatterns = format_suffix_patterns(urlpatterns)
