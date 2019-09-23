from box import Box
from faker import Faker

import random

fake = Faker()

therapists = []
patients = []


def fake_user():
  user = {
    "user": {
      "email": fake.email(),
      "firstName": fake.first_name(),
      "lastName": fake.last_name(),
      "password": fake.pystr(min_chars=10, max_chars=20),
      "gender": random.choice(['M', 'F'])
    }
  }
  return Box(user)


def fake_therapist():
  therapist = {
    "therapist": {
      "email": fake.email(),
      "firstName": fake.first_name(),
      "lastName": fake.last_name(),
      "password": fake.pystr(min_chars=10, max_chars=20)
    }
  }
  return Box(therapist)


def fake_device():
  device = {
    "fcmdevice_set": [{
      "registrationId": fake.uuid4(),
      "name": fake.user_name(),
      "active": True,
      "device_id": fake.uuid4(),
      "type": "android"
    }]
  }

  return Box(device)


def fake_address():
  address = {
    "addresses": [{
      "name": random.choice(["Home", "Work", "Dumpster"]),
      "text": fake.address(),
      "primary": True,
      "apartment": fake.numerify(text="##"),
      "location": {
        "type": "Point",
        "coordinates": [float(fake.longitude()), float(fake.latitude())]
      }
    }]
  }

  return Box(address)


def fake_patient_create_body():
  patient = {**fake_user(), **fake_device(), **fake_address()}
  patients.append(patient)
  return Box(patient)


def fake_therapist_create_body():
  therapist = {**fake_user(), **fake_therapist(), **fake_device(), **fake_address()}
  therapists.append(therapist)
  return Box(therapist)


def test_scope(request):
  return Box({"moca": globals()})
