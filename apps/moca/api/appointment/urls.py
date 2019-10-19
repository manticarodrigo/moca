from django.urls import path
from knox.views import LogoutView

from .views import AppointmentListCreateView, AppointmentAPIDetailView, ReviewAPIView, ReviewAPIDetailView

urlpatterns = [
  #create/search appointments
  path('', AppointmentListCreateView.as_view()),
  # retrieve/update/cancel appointments
  path('<int:appointment_id>', AppointmentAPIDetailView.as_view()),

  # create appointment review
  path('<int:appointment_id>/review', ReviewAPIView.as_view()),
  # retrieve/update/delete appointments
  path('<int:appointment_id>/review/<int:review_id>', ReviewAPIDetailView.as_view()),
  path('<int:appointment_id>/review/<int:review_id>', ReviewAPIDetailView.as_view()),
  path('<int:appointment_id>/review/<int:review_id>', ReviewAPIDetailView.as_view()),
]
