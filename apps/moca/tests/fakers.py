import random

from faker import Faker

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
