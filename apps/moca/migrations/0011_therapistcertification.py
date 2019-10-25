# Generated by Django 2.1.10 on 2019-10-25 05:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('moca', '0010_auto_20191025_0513'),
    ]

    operations = [
        migrations.CreateModel(
            name='TherapistCertification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('image', models.ImageField(null=True, upload_to='diagnosis')),
                ('therapist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certifications', to='moca.Therapist')),
            ],
        ),
    ]