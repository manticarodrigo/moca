import os
import stripe

from rest_framework.exceptions import APIException

from config.settings.base import get_service_host

STRIPE_API_KEY = os.environ.get('STRIPE_API_KEY')
STRIPE_CLIENT_ID = os.environ.get('STRIPE_CLIENT_ID')

stripe.api_key = STRIPE_API_KEY


def get_connect_oauth_url(user):
  base_url = 'https://connect.stripe.com/express/oauth/authorize'
  response_type = 'response_type=code'
  client_id = f'client_id={STRIPE_CLIENT_ID}'
  scope = 'scope=read_write'
  suggested_capabilities = 'suggested_capabilities[]=transfers'
  state = f'state={user.id}'
  redirect_uri = f'redirect_uri={get_service_host()}/api/payment/connect/callback/'
  email = f'stripe_user[email]={user.email}'
  first_name = f'stripe_user[first_name]={user.first_name}'
  last_name = f'stripe_user[last_name]={user.last_name}'
  country = f'stripe_user[country]=US'
  url = f'{base_url}?{response_type}&{client_id}&{scope}&{suggested_capabilities}&{state}&{redirect_uri}&{email}&{first_name}&{last_name}&{country}'
  return url

def get_connect_login_url(merchant_id):
  return stripe.Account.create_login_link(merchant_id)

def connect_account(code):
  try:
    response = stripe.OAuth.token(
      grant_type='authorization_code',
      code=code,
    )
    return response['stripe_user_id']
  except Exception as e:
    print('STRIPE CONNECT EXCEPTION', e)
    raise APIException('STRIPE ISSUE')


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
def charge_customer(customer_id, merchant_id, amount, description, currency='usd'):
  try:
    application_fee = int(amount * 0.15)
    charge = stripe.Charge.create(amount=amount,
                                  currency=currency,
                                  description=description,
                                  customer=customer_id,
                                  application_fee_amount=application_fee,
                                  transfer_data={'destination': merchant_id})
  except Exception as e:
    print('STRIPE CHARGE CARD EXCEPTION', e)
    raise APIException('STRIPE ISSUE')
