# Generated by Django 2.1.10 on 2019-10-21 21:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('moca', '0006_auto_20191021_1908'),
    ]

    operations = [
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=2)),
                ('zip_code', models.CharField(max_length=5)),
            ],
        ),
    ]
