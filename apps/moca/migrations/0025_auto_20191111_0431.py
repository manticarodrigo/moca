# Generated by Django 2.1.10 on 2019-11-11 04:31

from django.db import migrations, models


class Migration(migrations.Migration):

  dependencies = [
    ('moca', '0024_auto_20191110_0610'),
  ]

  operations = [
    migrations.RemoveField(
      model_name='appointment',
      name='is_cancelled',
    ),
    migrations.AddField(
      model_name='appointment',
      name='status',
      field=models.CharField(choices=[('in-progress', 'In Progress'),
                                      ('not-started', 'Not Started'), ('completed', 'Completed'),
                                      ('cancelled', 'Cancelled')],
                             default='not-started',
                             max_length=15),
    ),
  ]