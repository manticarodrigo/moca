from rest_framework import serializers, status

from rest_framework.exceptions import APIException
from moca.models.user.payment import Payment, PaymentProfile, Card, Bank, \
  PAYMENT_TYPE_BANK, PAYMENT_TYPE_CARD
from moca.services.stripe import create_customer, update_customer, add_payment, charge_customer


def get_model_and_serializer_by_type(type):
  if type == PAYMENT_TYPE_CARD:
    return Card, CardSerializer

  if type == PAYMENT_TYPE_BANK:
    return Bank, BankSerializer

  raise APIException("Unsupported payment type")


class CardSerializer(serializers.ModelSerializer):
  class Meta:
    model = Card
    exclude = ['id', 'user', 'payment', 'created_at']


class BankSerializer(serializers.ModelSerializer):
  class Meta:
    model = Bank
    exclude = ['id', 'user', 'payment', 'created_at']


class PaymentSerializer(serializers.ModelSerializer):
  type = serializers.StringRelatedField()
  name = serializers.StringRelatedField()
  payment_info = serializers.SerializerMethodField()

  class Meta:
    model = Payment
    exclude = ['user', 'created_at', 'token']

  def get_payment_info(self, obj):
    payment_type = obj.type
    payment_model, payment_serializer = get_model_and_serializer_by_type(payment_type)
    payment_info = payment_model.objects.get(payment=obj)
    return payment_serializer(payment_info).data

  def create(self, validated_data):
    request = self.context['request']
    user = request.user
    token = request.data['id']

    if request.data.get(PAYMENT_TYPE_CARD):
      payment_type = PAYMENT_TYPE_CARD
    elif request.data.get(PAYMENT_TYPE_BANK):
      payment_type = PAYMENT_TYPE_BANK
    else:
      raise APIException("Unsupported payment type")

    payment_model, _ = get_model_and_serializer_by_type(payment_type)

    validated_data['user'] = user
    validated_data['name'] = request.data[payment_type]['name']
    validated_data['token'] = token
    validated_data['type'] = payment_type

    try:
      payment_profile = PaymentProfile.objects.get(user=user)
      add_payment(payment_profile.stripe_customer_id, token=token)
    except PaymentProfile.DoesNotExist:
      customer = create_customer(email=user.email, name=user.get_full_name(), token=token)
      payment_profile = PaymentProfile.objects.create(user=user, stripe_customer_id=customer.id)

    payment = Payment.objects.create(**validated_data)

    payment_data = request.data[payment_type]
    # Support future updates to model
    model_fields = [f.name for f in payment_model._meta.get_fields() if not f.auto_created]
    fields = {field: payment_data[field] for field in model_fields if field in payment_data}
    payment_model.objects.create(**fields, payment=payment, user=user)

    return payment
