from rest_framework import status
from rest_framework.exceptions import APIException, NotFound, NotAcceptable


class AppointmentNotFound(NotFound):
  def __init__(self, id):
    self.detail = f'Appointment with id {id} not found'


class ReviewNotFound(NotFound):
  def __init__(self, id):
    self.detail = f'Review with id {id} not found'


class AppointmentAlreadyReviewed(NotAcceptable):
  def __init__(self, id):
    self.detail = f'Appointment with id {id} has already been rated.'
