# Generated by Django 2.1.10 on 2019-11-10 03:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('moca', '0022_lastseen'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='LastSeen',
            new_name='LastViewed',
        ),
    ]