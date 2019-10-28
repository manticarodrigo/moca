from box import Box
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from moca.tests.fakers import fake_address, fake_user
from moca.tests.patient_tests import PatientTests
from moca.tests.user_tests import UserTests


class TherapistTests(UserTests):
  def user_type(self):
    return "therapist"

  def create_user(self):
    return self.test_create_therapist().therapist

  def test_create_therapist(self):
    url = reverse('create-therapist')
    data = fake_user()
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    self.assertIn('id', response.data)
    self.assertEqual(type(response.data['id']), int)

    therapist = Box(response.data)
    therapist.password = data['user']['password']

    return Box({"therapist": therapist})
