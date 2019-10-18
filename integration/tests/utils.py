from box import Box
from faker import Faker
from datetime import datetime, timedelta

import random

fake = Faker()
fake.seed(9001)
random.seed(9001)

AILMENTS = [
  "Neck", "Shoulder", "Elbow", "Write/Hand", "Low Back", "Hip/Pelvis", "Knee", "Ankle/Foot",
  "Other"
]

SESSION_TYPES = ["thirty", "fourtyfive", "sixty", "evaluation"]

therapists = []
patients = []


def fake_user(gender=None):
  user = {
    "user": {
      "email": fake.email(),
      "firstName": fake.first_name(),
      "lastName": fake.last_name(),
      # "password": fake.pystr(min_chars=10, max_chars=20),
      "password": 'test1234',
      "gender": random.choice(['M', 'F']) if not gender else gender
    }
  }
  return Box(user)


def fake_therapist(ailments=None, tariffs=None):
  therapist = {
    "therapist": {
      "email": fake.email(),
      "firstName": fake.first_name(),
      "lastName": fake.last_name(),
      "password": 'test1234',
      "preferredAilments": random.choices(AILMENTS, k=random.randint(0, len(AILMENTS))),
    }
  }

  if ailments:
    therapist['therapist']['preferredAilments'] = ailments
  return Box(therapist)


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


def fake_addresses():
  address_count = random.randint(1, 3)
  addresses = {"addresses": list(map(lambda _: fake_address(), range(address_count)))}

  primary = random.choice(addresses['addresses'])
  primary['primary'] = True

  return Box(addresses)


def fake_patient_create_body():
  patient = fake_user()
  patients.append(patient)
  return Box(patient)


def fake_therapist_create_body(ailments=None, gender=None, tariffs=None):
  therapist = {
    **fake_user(gender),
    **fake_therapist(ailments, tariffs),
    **fake_addresses()
  }
  therapists.append(therapist)
  return Box(therapist)

def fake_review():
  review =  {
              "comment": fake.text(),
              "rating": round(random.uniform(0,5),2)
            }
  return Box(review)

def fake_end_time():
  return datetime.now() + timedelta(days=2, hours=1)

def fake_media_message():
  # todo use media_types
  media_types=['png','pdf','abc']
  message = {"type":"media",
                "data": {
                  "mediatype": "png",
                  "file": "011000111010110101",
                  "text": fake.text()
                }
             }
  return Box(message)

# todo
def fake_request_message(therapist_id,patient_id,patient_address_id):
  message = {"type":"request",
             "data": {
               "patient": patient_id,
               "therapist": therapist_id,
               "address": patient_address_id,
               "start_time": "2019-12-05T13:00:00",
               "end_time": "2019-12-05T13:00:00",
               "price": random.randint(50,100)
                }
             }
  return Box(message)

def fake_response_message(request_id,response):
  message = {"type":"response",
             "data": {
               "request_id": request_id ,
               "response": response
               }
             }
  return Box(message)
last_box = {}

def test_scope(response, **kwargs):
  global last_box
  save_as = kwargs.pop('save_as')

  saved_box = Box({
    **last_box, "globals": globals(),
    save_as: {
      **response.json(),
      **kwargs
    },
  })
  last_box = saved_box

  return saved_box


def return_(name=None):
  if name:
    return last_box[name]
  else:
    return {}
