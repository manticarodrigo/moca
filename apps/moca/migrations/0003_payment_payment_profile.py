# Generated by Django 2.1.10 on 2019-11-15 03:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moca', '0002_auto_20191115_0250'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='moca.PaymentProfile'),
        ),
    ]
