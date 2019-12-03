from django.core.management.base import BaseCommand

from moca.services.push import send_push_message


class Command(BaseCommand):
  def handle(self, *args, **options):
    try:
      send_push_message('ExponentPushToken[ALwN-8GC-sm3nBMJK0gigz]', 'Hello!!!')
      print("Push success!")
    except:
      print("Push failed!")
