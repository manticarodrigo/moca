from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from moca.models.user.user import Patient
from box import Box
from moca.tests.fakers import *


class PatientTests(APITestCase):
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

  def test_patient_login(self):
    patient = self.test_create_patient().patient
    url = reverse('knox_login')

    # Test failed login
    credentials = {"email": patient.email, "password": patient.password}
    credentials['password'] = credentials['password'] + 'x'
    response = self.client.post(url, credentials, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test successful login
    credentials = {"email": patient.email, "password": patient.password}
    response = self.client.post(url, credentials, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn("token", response.data)

    return Box({"token": response.data['token'], "patient": patient})

  def test_address_creation(self):
    patient = self.test_patient_login()

    url = reverse('create-address')
    address = fake_address()

    self.client.credentials(HTTP_AUTHORIZATION=f'Token {patient.token}')
    response = self.client.post(url, address, format='json')

    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    return Box({"token": patient.token, "patient": patient.patient, "address": response.data})
