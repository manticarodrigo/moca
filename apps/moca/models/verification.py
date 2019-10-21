from django.conf import settings
from django.db import models


class EmailVerification(models.Model):
  EXPIRED, PENDING, VERIFIED = 'EXPIRED', 'PENDING', 'VERIFIED'
  VERIFICATION_STATUS = [(EXPIRED, 'Expired'), (PENDING, 'Pending'), (VERIFIED, 'Verified')]

  token = models.CharField(max_length=100)
  user = models.ForeignKey(settings.AUTH_USER_MODEL,
                           related_name="email_verification_tokens",
                           on_delete=models.CASCADE)
  status = models.CharField(choices=VERIFICATION_STATUS, max_length=8, default=PENDING)
  created_at = models.DateTimeField(auto_now=True)
