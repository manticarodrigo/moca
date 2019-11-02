from box import Box
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from moca.models.app_availability import Area
from moca.tests.fakers import fake_address, fake_user


class TestBase(APITestCase):
  def get_test_instance(self, test):
    tests = test()
    tests.client = self.client
    return tests


class UserTests(TestBase):
  def create_user(self):
    pass

  def user_type(self):
    pass

  def test_login(self):
    if type(self) == UserTests:
      return
    user = self.create_user()
    url = reverse('knox_login')

    # Test failed login
    credentials = {"email": user.email, "password": user.password}
    credentials['password'] = credentials['password'] + 'x'
    response = self.client.post(url, credentials, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # Test successful login
    credentials = {"email": user.email, "password": user.password}
    response = self.client.post(url, credentials, format='json')
    self.assertEqual(response.status_code, status.HTTP_200_OK)
    self.assertIn("token", response.data)

    return Box({"token": response.data['token'], self.user_type(): user})

  def test_address_creation(self):
    if type(self) == UserTests:
      return
    user = self.test_login()
    url = reverse('create-address')
    address = fake_address()

    self.client.credentials(HTTP_AUTHORIZATION=f'Token {user.token}')

    response = self.client.post(url, address, format='json')
    self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    Area.objects.create(state=address['state'])

    response = self.client.post(url, address, format='json')
    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    return Box({"token": user.token, "user": user.get(self.user_type()), "address": response.data})
