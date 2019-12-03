from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response

from moca.models import User, EmailVerification, Device
from moca.services import canned_messages
from moca.services.emails import send_email
from moca.services.push import send_push_message


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def verify_email(request, token):
  email_verification = get_object_or_404(EmailVerification, token=token)
  if email_verification.status not in (EmailVerification.EXPIRED, EmailVerification.VERIFIED):
    email_verification.status = EmailVerification.VERIFIED
    email_verification.save()

    email_verification.user.is_active = True
    email_verification.user.save()

    if email_verification.user.type == User.PATIENT_TYPE:
      send_email(email_verification.user, **canned_messages.WELCOME_PATIENT)
    elif email_verification.user.type == User.THERAPIST_TYPE:
      send_email(email_verification.user, **canned_messages.WELCOME_PHYSICAL_THERAPIST)

    
    user_id = email_verification.user.id
    devices = Device.objects.filter(user=user_id)
    text = f'Your email was successfully verified.'

    for device in devices:
      send_push_message(device.token, text, {
        'type': 'email_verified',
        'params': {
          'user': {
            'id': user_id
          }
        }
      })

    # TODO this should be a rendered template or a redirect(which should open the app)
    return Response("Verified")
  else:
    # TODO this should be a rendered template
    return Response("Token expired")