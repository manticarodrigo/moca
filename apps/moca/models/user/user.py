import datetime

from knox.models import AuthToken
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from django.contrib.gis.db import models as gisModels
from django.contrib.gis.geos import Point
from django.contrib.postgres.fields import JSONField, ArrayField
from django.db import models
from django.db.models import Avg
from django.utils.translation import ugettext_lazy as _
from moca.models.appointment import Review


class EmailField(models.EmailField):
  def get_prep_value(self, value):
    value = super(EmailField, self).get_prep_value(value)
    if value is not None:
      value = value.lower()
    return value


class MyUserManager(BaseUserManager):
  """
  A custom user manager to deal with emails as unique identifiers for auth
  instead of usernames. The default that's used is "UserManager"
  """
  def _create_user(self, email, password, **extra_fields):
    """
    Creates and saves a User with the given email and password.
    """
    if not email:
      raise ValueError("The Email must be set")
    email = self.normalize_email(email)
    user = self.model(email=email, **extra_fields)
    user.set_password(password)
    setattr(user, 'created_at', datetime.datetime.now)
    user.save()
    return user

  def create_user(self, email, password=None, **extra_fields):
    """Create and save a regular User with the given email and password."""
    extra_fields.setdefault('is_staff', False)
    extra_fields.setdefault('is_superuser', False)
    return self._create_user(email, password, **extra_fields)

  def create_superuser(self, email, password, **extra_fields):
    # TODO
    # probably move to _create_user
    import datetime
    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault("is_superuser", True)
    extra_fields.setdefault("is_active", True)
    extra_fields.setdefault("gender", "M")
    extra_fields.setdefault("first_name", "admin")
    extra_fields.setdefault("last_name", "admin")
    extra_fields.setdefault("date_of_birth", datetime.datetime.now())
    extra_fields.setdefault("type", "AD")

    if extra_fields.get("is_staff") is not True:
      raise ValueError("Superuser must have is_staff=True.")
    if extra_fields.get("is_superuser") is not True:
      raise ValueError("Superuser must have is_superuser=True.")
    return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
  PATIENT_TYPE, THERAPIST_TYPE, AGENT_TYPE, ADMIN_TYPE = "PA", "PT", "AG", "AD"
  FEMALE, MALE = "F", "M"
  GENDERS = [(FEMALE, "Female"), (MALE, "Male")]

  USER_TYPES = [
    (PATIENT_TYPE, "Patient"),
    (THERAPIST_TYPE, "Physical Therapist"),
    (AGENT_TYPE, "Agent"),
    (ADMIN_TYPE, "Admin"),
  ]

  first_name = models.CharField(null=True, blank=True, max_length=50)
  last_name = models.CharField(null=True, blank=True, max_length=50)
  gender = models.CharField(max_length=2, choices=GENDERS, null=True, blank=True)
  date_of_birth = models.DateField(null=True, blank=True)
  # todo needs to be non-null field
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
  type = models.CharField(max_length=2, choices=USER_TYPES, default=AGENT_TYPE)
  image = models.ImageField(upload_to='users', blank=True, null=True)

  email = EmailField(unique=True, null=True)
  is_staff = models.BooleanField(
    _("staff status"),
    default=False,
    help_text=_("Designates whether the user can log into this site."),
  )
  is_active = models.BooleanField(
    _("active"),
    default=True,
    help_text=_("Designates whether this user should be treated as active. "
                "Unselect this instead of deleting accounts."),
  )

  USERNAME_FIELD = "email"
  objects = MyUserManager()

  def __str__(self):
    return f"{self.get_full_name()} - {self.email}"

  def get_full_name(self):
    return f"{self.first_name} {self.last_name}"

  def get_short_name(self):
    return f"{self.first_name}"

  def get_profile_model(self):
    if self.type == self.PATIENT_TYPE:
      return Patient
    if self.type == self.THERAPIST_TYPE:
      return Therapist

  def get_profile_type(self):
    if self.type == self.PATIENT_TYPE:
      return 'patient'
    if self.type == self.THERAPIST_TYPE:
      return 'therapist'


class PatientManager(MyUserManager):
  pass


class Patient(models.Model):
  user = models.OneToOneField(User,
                              on_delete=models.CASCADE,
                              primary_key=True,
                              related_name="patient")
  objects = PatientManager()


class TherapistManager(MyUserManager):
  pass


class Therapist(models.Model):
  user = models.OneToOneField(User,
                              on_delete=models.CASCADE,
                              primary_key=True,
                              related_name="therapist")
  AVAILABLE, BUSY = 'A', 'B'
  STATUS = [(AVAILABLE, 'Available'), (BUSY, 'Busy')]
  bio = models.CharField(max_length=200, blank=True, null=True)
  cert_date = models.DateField(blank=True, null=True)
  license_number = models.CharField(max_length=50, blank=True, null=True)
  is_verified = models.BooleanField(default=False)
  operation_radius = models.IntegerField(default=10)
  status = models.CharField(max_length=100, choices=STATUS, default=AVAILABLE)
  primary_location = gisModels.PointField(null=True)
  rating = models.FloatField(default=0)
  review_count = models.IntegerField(default=0)
  preferred_ailments = ArrayField(models.CharField(max_length=20), size=20, default=list)

  objects = TherapistManager()

  def update_rating(self):
    new_rating = Review.objects.filter(therapist=self).aggregate(Avg('rating'))['rating__avg']
    self.review_count = Review.objects.filter(therapist=self).count()
    self.rating = new_rating
    self.save()

  def __str__(self):
    return f'Therapist Object user: {self.user} bio : {self.bio} cert_date : {self.cert_date} \
      operation_radius : {self.operation_radius } \
      preferred_ailments : {self.preferred_ailments } \
      status: {self.status} '
