from box import Box
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from moca.tests.fakers import fake_address, fake_user
from moca.tests.user_create.patient_create_tests import PatientTests, MocaBase


class TherapistTests(PatientTests, MocaBase):
  def test_create_patient(self):
    url = reverse('create-patient')
    data = fake_user()
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertIn('id', response.data)
    self.assertEqual(type(response.data['id']), int)

    patient = Box(response.data)
    patient.password = data['user']['password']

    return Box({"patient": patient})
