# Generated by Django 2.1.10 on 2019-08-26 02:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moca', '0004_auto_20190824_2255'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='address',
            name='city',
        ),
        migrations.RemoveField(
            model_name='address',
            name='state',
        ),
        migrations.RemoveField(
            model_name='address',
            name='street',
        ),
        migrations.RemoveField(
            model_name='address',
            name='zip_code',
        ),
        migrations.AddField(
            model_name='address',
            name='text',
            field=models.CharField(default='', max_length=300),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL),
        ),
    ]
