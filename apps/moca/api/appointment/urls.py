from django.urls import path
from knox.views import LogoutView

from .views import (AppointmentAPIDetailView, AppointmentListView, AppointmentRequestView,
                    AppointmentCancelView, AppointmentStartView, AppointmentEndView)

urlpatterns = [
  path('', AppointmentListView.as_view(), name='create-appointment'),
  path('<int:appointment_id>/', AppointmentAPIDetailView.as_view(), name='appointment-detail'),
  path('<int:appointment_id>/cancel/', AppointmentCancelView.as_view(), name='appointment-cancel'),
  path('<int:appointment_id>/start/', AppointmentStartView.as_view(), name='appointment-cancel'),
  path('<int:appointment_id>/end/', AppointmentEndView.as_view(), name='appointment-cancel'),
  path('request/<int:appointment_request_id>/<slug:request_status>/',
       AppointmentRequestView.as_view(),
       name='reply-appointment')
]
