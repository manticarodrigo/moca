from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response

from moca.models import User, EmailVerification
from moca.services import canned_messages
from moca.services.emails import send_email


@api_view(['GET'])
def verify_email(request, token):
  emailVerification = get_object_or_404(EmailVerification, token=token)
  if emailVerification.status not in (EmailVerification.EXPIRED, EmailVerification.VERIFIED):
    emailVerification.status = EmailVerification.VERIFIED
    emailVerification.save()

    emailVerification.user.is_active = True
    emailVerification.user.save()

    if emailVerification.user.type == User.PATIENT_TYPE:
      send_email(emailVerification.user, **canned_messages.WELCOME_PATIENT)
    elif emailVerification.user.type == User.THERAPIST_TYPE:
      send_email(emailVerification.user, **canned_messages.WELCOME_PHYSICAL_THERAPIST)

    # TODO this should be a rendered template or a redirect(which should open the app)
    return Response("Verified")
  else:
    # TODO this should be a rendered template
    return Response("Token expired")