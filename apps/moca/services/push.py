from exponent_server_sdk import PushClient, PushMessage


def send_push_message(token, message, extra=None):
  """
  Basic arguments. You should extend this function with the push features you
  want to use, or simply pass in a `PushMessage` object.
  """
  try:
    PushClient().publish(PushMessage(to=token, body=message, data=extra))
  except Exception as exc:
    print("Push notification error:", exc)
