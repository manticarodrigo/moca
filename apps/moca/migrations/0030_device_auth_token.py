# Generated by Django 2.1.10 on 2019-11-13 04:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('knox', '0007_auto_20190111_0542'),
        ('moca', '0029_address_archive'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='auth_token',
            field=models.ForeignKey(default='f8145f9c04c3691b5af49e1535f95f819adf504cc8dc881097cff205d7b165c9ac0fa081a620768829198f8a42d17a5f5dfacee7b5e394c1f7bef602e7acff81', on_delete=django.db.models.deletion.CASCADE, to='knox.AuthToken'),
            preserve_default=False,
        ),
    ]
