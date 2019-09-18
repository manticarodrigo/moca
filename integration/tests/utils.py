from box import Box
from faker import Faker

fake = Faker()


def fake_user():
  user = {
    "user": {
      "email": fake.email(),
      "firstName": fake.first_name(),
      "lastName": fake.last_name(),
      "password": fake.pystr(min_chars=10, max_chars=20)
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
      "name": "Home",
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
  return Box({**fake_user(), **fake_device(), **fake_address()})

def fake_therapist_create_body():
  return Box({**fake_user(), **fake_therapist(), **fake_device(), **fake_address()})
