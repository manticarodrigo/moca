# Generated by Django 2.1.10 on 2019-09-11 08:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moca', '0005_auto_20190911_0834'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
