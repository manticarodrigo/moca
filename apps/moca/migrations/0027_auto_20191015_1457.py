# Generated by Django 2.1.10 on 2019-10-15 14:57

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moca', '0026_auto_20191015_1455'),
    ]

    operations = [
        migrations.AlterField(
            model_name='therapist',
            name='preferred_ailments',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), default=[], size=20),
        ),
    ]
