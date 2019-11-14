# Create your tasks here
from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def send_appt_start_notification(appointment_id, therapist_id, patient_id):
  try:
    print("APPT", appointment_id, "Therapist", therapist_id, "Patient", patient_id)
  except:
    print("Handle Errors")
