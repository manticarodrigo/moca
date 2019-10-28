from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from moca.models.user.user import Patient
from box import Box

from faker import Faker

import random

fake = Faker()
fake.seed(9001)
random.seed(9001)


def fake_user(gender=None):
  return {
    "user": {
      "email": fake.email(),
      "firstName": fake.first_name(),
      "lastName": fake.last_name(),
      "password": fake.pystr(min_chars=10, max_chars=20),
      "gender": random.choice(['M', 'F']) if not gender else gender
    }
  }


def fake_address():
  return {
    "primary": True,
    "name": random.choice(["Home", "Work", "Dumpster"]),
    "street": fake.street_address(),
    "apartment": fake.numerify(text="##"),
    "zip_code": fake.postcode(),
    "city": fake.city(),
    "state": fake.state_abbr(),
    "location": {
      "type": "Point",
      "coordinates": [float(fake.longitude()), float(fake.latitude())]
    }
  }


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

    return patient

  def test_patient_login(self):
    patient = self.test_create_patient()
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

    return (response.data['token'], patient)

  def test_address_creation(self):
    (token, patient) = self.test_patient_login()

    url = reverse('create-address')
    address = fake_address()

    self.client.credentials(HTTP_AUTHORIZATION=f'Token {token}')
    self.client.post(url, address, format='json')
