# Generated by Django 2.1.10 on 2019-09-11 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moca', '0002_patient_therapist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='date_of_birth',
            field=models.DateField(blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='gender',
            field=models.CharField(blank=True, choices=[('F', 'Female'), ('M', 'Male')], max_length=2),
        ),
    ]
