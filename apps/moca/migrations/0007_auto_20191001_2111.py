# Generated by Django 2.1.10 on 2019-10-01 21:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moca', '0006_auto_20191001_2014'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.FloatField(),
        ),
    ]