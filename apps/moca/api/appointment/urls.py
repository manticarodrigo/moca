from django.urls import path
from knox.views import LogoutView

from .views import (AppointmentAPIDetailView, AppointmentListView,
                    AppointmentRequestView)

urlpatterns = [
  path('', AppointmentListView.as_view(), name='create-appointment'),
  path('<int:appointment_id>/', AppointmentAPIDetailView.as_view(), name='appointment-detail'),
  path('request/<int:appointment_request_id>/<slug:request_status>/',
       AppointmentRequestView.as_view(),
       name='reply-appointment')
]
