from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from moca.models.user.user import Patient
from box import Box
from .fakers import *
from .therapist_tests import TherapistTests
from .patient_tests import PatientTests


class AppointmentCreateTests(PatientTests, TherapistTests):
  def test_appointment_create(self):
    patient = super(TherapistTests, self).test_address_creation()
