import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.postgres.fields import JSONField
from django.conf import settings
from django.contrib.auth.models import (
  BaseUserManager,
  AbstractBaseUser,
  PermissionsMixin,
)


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
    print('in _create_user0')
    setattr(user, 'created_at', datetime.datetime.now)
    print('in _create_user1')
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
  FEMALE, MALE = "F", "M"
  GENDERS = [(FEMALE, "Female"), (MALE, "Male")]

  PATIENT, THERAPIST, AGENT, ADMIN = "PA", "PT", "AG", "AD"
  USER_TYPES = [
    (PATIENT, "Patient"),
    (THERAPIST, "Physical Therapist"),
    (AGENT, "Agent"),
    (ADMIN, "Admin"),
  ]

  first_name = models.CharField(null=True, blank=True, max_length=50)
  last_name = models.CharField(null=True, blank=True, max_length=50)
  gender = models.CharField(max_length=2, choices=GENDERS, null=True, blank=True)
  date_of_birth = models.DateField(null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
  type = models.CharField(max_length=2, choices=USER_TYPES, default=AGENT)

  email = models.EmailField(unique=True, null=True)
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
    return f'id:{self.id}, email:{self.email}, first_name:{self.first_name}, last_name:{self.last_name}' \
           f'gender:{self.gender}, date_of_birth:{self.date_of_birth},created_at:{self.created_at}'

  def get_full_name(self):
    return self.email

  def get_short_name(self):
    return self.email


class PatientManager(MyUserManager):
  pass


class Patient(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  objects = MyUserManager


class TherapistManager(MyUserManager):
  pass


class Therapist(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
  AVAILABLE, BUSY = 'A', 'B'
  QUALIFICATIONS = [
    'Ankle/Foot', 'Arm', 'Hip', 'Knee', 'Lower Back', 'Neck', 'Pelvis', 'Shoulder', 'Upper Back',
    'Other'
  ]
  STATUS = [(AVAILABLE, 'Available'), (BUSY, 'Busy')]
  bio = models.CharField(max_length=200, blank=True, null=True)
  cert_date = models.DateField(blank=True, null=True)
  operation_radius = models.IntegerField(default=10)
  qualifications = JSONField(default=dict)
  interests = models.CharField(max_length=100, blank=True, null=True)
  status = models.CharField(max_length=100, choices=STATUS, default=AVAILABLE)

  objects = TherapistManager()
