from celery import shared_task

from .models import Device, Appointment
from moca.services.notification.push import send_push_message


@shared_task
def send_appt_start_notification(appointment_id):
  try:
    appointment = Appointment.objects.get(id=appointment_id)

    therapist_name = appointment.therapist.user.get_full_name()
    patient_name = appointment.patient.user.get_full_name()

    # Therapist
    devices = Device.objects.filter(user_id=appointment.therapist_id)
    text = f'Your appointment with {patient_name} is starting soon.'

    for device in devices:
      send_push_message(device.token, text, {
        'type': 'start_appointment',
      })

    # Patient
    devices = Device.objects.filter(user_id=appointment.patient_id)
    text = f'Your appointment with {therapist_name} is starting soon.'

    for device in devices:
      send_push_message(device.token, text, {
        'type': 'start_appointment',
      })

  except:
    print("Handle Errors")


@shared_task
def send_appt_review_notification(appointment_id):
  try:
    appointment = Appointment.objects.get(id=appointment_id)
    therapist_name = appointment.therapist.user.get_full_name()

    devices = Device.objects.filter(user_id=appointment.patient_id)
    text = f'Please review your appointment with {therapist_name}.'

    for device in devices:
      send_push_message(device.token, text, {
        'type': 'review_appointment',
      })

  except:
    print("Handle Errors")
