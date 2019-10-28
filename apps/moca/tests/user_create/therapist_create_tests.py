from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from box import Box

from moca.tests.fakers import fake_address, fake_user
from moca.tests.user_create.patient_create_tests import PatientTests


class TherapistTests(PatientTests):
  pass
