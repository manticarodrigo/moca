from django.urls import path

from .views import (AppointmentListView, AppointmentDetailView, AppointmentNoteView,
                    AppointmentNoteImageDestroyView, AppointmentRequestView, AppointmentCancelView,
                    AppointmentStartView, AppointmentEndView)

urlpatterns = [
  path('', AppointmentListView.as_view(), name='create-appointment'),
  path('<int:appointment_id>/', AppointmentDetailView.as_view(), name='appointment-detail'),
  path('<int:appointment_id>/note/', AppointmentNoteView.as_view(), name='appointment-note'),
  path('<int:appointment_id>/note/image/<int:image_id>/', AppointmentNoteImageDestroyView.as_view(),
       name='appointment-note-image-destroy'),
  path('<int:appointment_id>/cancel/', AppointmentCancelView.as_view(), name='appointment-cancel'),
  path('<int:appointment_id>/start/', AppointmentStartView.as_view(), name='appointment-start'),
  path('<int:appointment_id>/end/', AppointmentEndView.as_view(), name='appointment-end'),
  path('request/<int:appointment_request_id>/<slug:request_status>/',
       AppointmentRequestView.as_view(),
       name='reply-appointment')
]
