from django.urls import path
from knox.views import LogoutView

from .views import AppointmentListView, AppointmentAPIDetailView, AppointmentRequestView

urlpatterns = [
  path('', AppointmentListView.as_view()),
  path('<int:appointment_id>', AppointmentAPIDetailView.as_view()),
  path('request/<int:appointment_request_id>/<slug:request_status>/', 
       AppointmentRequestView.as_view())
]
