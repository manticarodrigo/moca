# Generated by Django 2.1.10 on 2019-10-22 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moca', '0003_auto_20191022_2121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='therapist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='moca.Therapist'),
        ),
    ]
