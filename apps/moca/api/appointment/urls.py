from django.urls import path
from knox.views import LogoutView

from .views import AppointmentListCreateView, AppointmentAPIDetailView

urlpatterns = [
  path('', AppointmentListCreateView.as_view()),
  path('<int:appointment_id>', AppointmentAPIDetailView.as_view())
]
