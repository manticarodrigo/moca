from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.db.models import signals
from moca.services.stripe import remove_payment
from rest_framework.exceptions import ValidationError

PAYMENT_TYPE_BANK = 'bank_account'
PAYMENT_TYPE_CARD = 'card'


class PaymentProfile(models.Model):
  stripe_customer_id = models.CharField(max_length=20)
  user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

  def __str__(self):
    return f"Payment Profile: {self.id}, User: {self.user}"


class Payment(models.Model):
  PAYMENT_TYPES = [(PAYMENT_TYPE_BANK, 'Bank'), (PAYMENT_TYPE_CARD, 'Card')]

  primary = models.BooleanField(default=False)
  name = models.CharField(max_length=20, null=True)
  user = models.ForeignKey(settings.AUTH_USER_MODEL,
                           related_name="payments",
                           on_delete=models.CASCADE)
  payment_profile = models.ForeignKey(PaymentProfile,
                                      related_name="payments",
                                      on_delete=models.CASCADE,
                                      null=True)
  created_at = models.DateTimeField(auto_now_add=True)
  type = models.CharField(max_length=15, choices=PAYMENT_TYPES)
  token = models.CharField(max_length=30)

  def __str__(self):
    return f"Payment: {self.id}, User: {self.user}"


@receiver(signals.pre_delete, sender=Payment)
def payment_pre_delete(sender, instance, *args, **kwargs):
  payment = instance

  if payment.primary:
    raise ValidationError('Can not delete primary payment.')

  customer_id = payment.payment_profile.stripe_customer_id
  if payment.type == PAYMENT_TYPE_CARD:
    payment_token = payment.card.token

  if payment.type == PAYMENT_TYPE_BANK:
    payment_token = payment.bank.token

  if payment_token:
    remove_payment(customer_id, payment_token)


class Card(models.Model):
  VISA = 'Visa'
  MASTERCARD = 'MasterCard'
  AMEX = 'American Express'
  DISCOVER = 'Discover'
  JCB = 'JCB'
  DINERS_CLUB = 'Diners Club'
  UNION_PAY = 'UnionPay'
  UNKOWN = 'Unknown'

  CARD_TYPES = [(VISA, 'Visa'), (MASTERCARD, 'Mastercard'), (AMEX, 'Amex'), \
                (DISCOVER, 'Discover'), (JCB, 'JCB'), (DINERS_CLUB, 'Diners Club'), \
                (UNION_PAY, 'UnionPay'), (UNKOWN, 'Unknown')]

  user = models.ForeignKey(settings.AUTH_USER_MODEL,
                           related_name="cards",
                           on_delete=models.CASCADE)
  payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name="card")
  created_at = models.DateTimeField(auto_now_add=True)
  exp_year = models.CharField(max_length=4)
  exp_month = models.CharField(max_length=2)
  last_4 = models.CharField(max_length=4)
  brand = models.CharField(max_length=10, choices=CARD_TYPES)
  token = models.CharField(max_length=30)

  def __str__(self):
    return f"Card: XXXX-XXXX-XXXX-{self.last_4}, User: {self.user}"


class Bank(models.Model):
  user = models.ForeignKey(settings.AUTH_USER_MODEL,
                           related_name="banks",
                           on_delete=models.CASCADE)
  payment = models.OneToOneField(Payment, on_delete=models.CASCADE, related_name="bank")
  created_at = models.DateTimeField(auto_now_add=True)
  account_holder_name = models.CharField(max_length=20)
  bank_name = models.CharField(max_length=20)
  routing_number = models.CharField(max_length=20)
  last_4 = models.CharField(max_length=4)
  token = models.CharField(max_length=30)

  def __str__(self):
    return f"Bank: {self.bank_name}, User: {self.user}"
