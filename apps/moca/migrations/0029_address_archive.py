# Generated by Django 2.1.10 on 2019-11-13 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moca', '0028_remove_device_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='archive',
            field=models.BooleanField(default=False),
        ),
    ]
