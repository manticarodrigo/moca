# Generated by Django 2.1.10 on 2019-11-15 04:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moca', '0003_payment_payment_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='bank',
            name='token',
            field=models.CharField(default='1', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='card',
            name='token',
            field=models.CharField(default='1', max_length=30),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bank',
            name='payment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bank', to='moca.Payment'),
        ),
        migrations.AlterField(
            model_name='card',
            name='payment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='card', to='moca.Payment'),
        ),
    ]
