from django.db import models
from django.utils.translation import ugettext_lazy as _
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

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    gender = models.CharField(max_length=2, choices=GENDERS)
    date_of_birth = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
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
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )

    USERNAME_FIELD = "email"
    objects = MyUserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email
