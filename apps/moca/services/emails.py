import random
import string
from os import environ

from django.core import mail
from django.core.mail import send_mail

from config.settings.base import get_service_host
from moca.models import EmailVerification


def send_email(user, subject, body):
  with mail.get_connection() as connection:
    mail.EmailMessage(
      subject,
      body,
      "Moca",
      [user.email],
      connection=connection,
    ).send()


def send_verification_mail(user):
  token_chars = string.ascii_letters + string.digits
  token = "".join(list(map(lambda _: random.choice(token_chars), range(0, 100))))

  EmailVerification.objects.create(token=token, user=user)

  url = f'{get_service_host()}/api/user/verify/{token}'

  send_email(
    user,
    'Verify your email',
    f'Please confirm your email by clicking here: {url}',
  )
