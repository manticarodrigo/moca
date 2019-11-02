from box import Box
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from moca.models.user.user import Patient

from .fakers import *
from .patient_tests import PatientTests
from .therapist_tests import TherapistTests


class AppointmentCreateTests(PatientTests, TherapistTests):
  # def create_chat(therapist, patient):
  def test_appointment_create(self):
    patient = self.get_test_instance(PatientTests).test_address_creation()
    therapist = self.get_test_instance(TherapistTests).test_address_creation()
    url = reverse('send-message', kwargs={"user_id": patient.user.id})
    appointmentRequest = {
      'type': 'appointment-request',
      'content': {
        "startTime": "2019-11-11T10:00",
        "endTime": "2019-11-11T11:00",
        "price": 100,
        "patient": int(patient.user.id),
        "therapist": int(therapist.user.id)
      }
    }

    self.client.credentials(HTTP_AUTHORIZATION=f'Token {therapist.token}')
    response = self.client.post(url, appointmentRequest, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
