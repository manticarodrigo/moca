from celery import shared_task

from .models import Device, Appointment
from moca.services.push import send_push_message


@shared_task
def send_appt_upcoming_notification(appointment_id):
  try:
    appointment = Appointment.objects.get(id=appointment_id)

    therapist_name = appointment.therapist.user.get_full_name()
    patient_name = appointment.patient.user.get_full_name()

    # Therapist
    devices = Device.objects.filter(user_id=appointment.therapist_id)
    text = f'Your appointment with {patient_name} is starting soon.'

    for device in devices:
      send_push_message(device.token, text, {
        'type': 'upcoming_appointment',
      })

    # Patient
    devices = Device.objects.filter(user_id=appointment.patient_id)
    text = f'Your appointment with {therapist_name} is starting soon.'

    for device in devices:
      send_push_message(device.token, text, {
        'type': 'upcoming_appointment',
      })

  except:
    print("Handle Errors")


@shared_task
def send_appt_start_notification(appointment_id):
  try:
    appointment = Appointment.objects.get(id=appointment_id)

    therapist_name = appointment.therapist.user.get_full_name()
    patient_name = appointment.patient.user.get_full_name()

    type = 'start_appointment'
    if appointment.status == 'payment-failed':
      type = 'failed_payment'

    # Therapist
    devices = Device.objects.filter(user_id=appointment.therapist_id)
    text = f'Your appointment with {patient_name} has started.'

    for device in devices:
      send_push_message(device.token, text, {
        'type': type,
      })

    # Patient
    devices = Device.objects.filter(user_id=appointment.patient_id)
    text = f'Your appointment with {therapist_name} has started.'

    for device in devices:
      send_push_message(device.token, text, {
        'type': type,
      })

  except:
    print("Handle Errors")


@shared_task
def send_appt_review_notification(appointment_id):
  try:
    appointment = Appointment.objects.get(id=appointment_id)

    if appointment.status != "in-progress" and appointment.status != "completed":
      # appointment cancelled. abort notification
      return

    if appointment.status == "in-progress":
      appointment.status = "completed"
      appointment.save()

    therapist_name = appointment.therapist.user.get_full_name()

    devices = Device.objects.filter(user_id=appointment.patient_id)
    text = f'Please review your appointment with {therapist_name}.'

    for device in devices:
      send_push_message(device.token, text, {
        'type': 'review_appointment',
        'params': {
          'appointment': {
            'id': appointment.id
          }
        }
      })

  except:
    print("Handle Errors")
