# Generated by Django 2.1.10 on 2019-11-09 01:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moca', '0018_merge_20191030_2256'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentCancellation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_processed', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('standard', 'Standard Cancellation Policy'), ('reschedule', 'Rescheduling'), ('weather', 'Cancellation Due to Weather'), ('emergency', 'Cancellation Due to an Emergency')], max_length=10)),
                ('description', models.TextField(blank=True)),
                ('cancellation_time', models.DateTimeField(auto_now_add=True)),
                ('appointment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='moca.Appointment')),
            ],
        ),
    ]