import stripe
from rest_framework.exceptions import APIException

stripe.api_key = 'sk_test_ZNk6P5iWYhDBBWIDcK7hZd1O00je2Z70F4'


def create_customer(**args):
  try:
    token = args.pop('token')
    customer = stripe.Customer.create(source=token, **args)
    return customer
  except Exception as e:
    print('STRIPE CREATE EXCEPTION', e)
    raise APIException('STRIPE ISSUE')


def get_customer(id):
  try:
    customer = stripe.Customer.retrieve(id)
    return customer
  except Exception as e:
    print('STRIPE GET CUSTOMER EXCEPTION', e)
    raise APIException('STRIPE ISSUE')


def add_payment(id, **args):
  try:
    token = args.pop('token')
    customer = stripe.Customer.create_source(id, source=token, **args)
    return customer
  except Exception as e:
    print('STRIPE ADD PAYMENT EXCEPTION', e)
    raise APIException('STRIPE ISSUE')


def remove_payment(customer_id, token):
  try:
    customer = stripe.Customer.delete_source(customer_id, token)
    return customer
  except Exception as e:
    print('STRIPE DELETE PAYMENT EXCEPTION', e)
    raise APIException('STRIPE ISSUE')


def set_primary_payment(customer_id, token):
  try:
    customer = stripe.Customer.modify(customer_id, default_source=token)
    return customer
  except Exception as e:
    print('STRIPE UPDATE PRIMARY PAYMENT EXCEPTION', e)
    raise APIException('STRIPE ISSUE')


# Amount is in cents!!!
def charge_customer(id, amount, description, currency='usd'):
  try:
    charge = stripe.Charge.create(amount=amount,
                                  currency=currency,
                                  description=description,
                                  customer=id)
  except Exception as e:
    print('STRIPE CHARGE CARD EXCEPTION', e)
    raise APIException('STRIPE ISSUE')
