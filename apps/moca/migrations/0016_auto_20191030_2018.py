# Generated by Django 2.1.10 on 2019-10-30 20:18

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moca', '0015_remove_therapist_qualifications'),
    ]

    operations = [
        migrations.CreateModel(
            name='Injury',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
                ('images', django.contrib.postgres.fields.ArrayField(base_field=models.ImageField(upload_to='injuries'), null=True, size=None)),
                ('patient', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='moca.Patient')),
            ],
        ),
        migrations.RemoveField(
            model_name='diagnosis',
            name='patient',
        ),
        migrations.DeleteModel(
            name='Diagnosis',
        ),
    ]