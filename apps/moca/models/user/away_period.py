from django.db import models

from .user import Therapist


class AwayPeriod(models.Model):
  therapist = models.ForeignKey(Therapist,
                                on_delete=models.CASCADE,
                                primary_key=False,
                                related_name='away_days')
  start_date = models.DateTimeField()
  end_date = models.DateTimeField()

  def __str__(self):
    return f'Therapist: {self.therapist.user.first_name} {self.therapist.user.last_name} \
             Start: {self.start_date} End: {self.end_date}'
