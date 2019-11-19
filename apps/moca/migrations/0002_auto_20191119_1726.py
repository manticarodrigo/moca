# Generated by Django 2.1.10 on 2019-11-19 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('knox', '0007_auto_20190111_0542'),
        ('moca', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.CharField(choices=[('high', 'high'), ('normal', 'normal'), ('low', 'low')], default='normal', max_length=20)),
                ('description', models.TextField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='NoteImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='notes')),
            ],
        ),
        migrations.RemoveField(
            model_name='note',
            name='files',
        ),
        migrations.AddField(
            model_name='bank',
            name='token',
            field=models.CharField(default='12345', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='card',
            name='token',
            field=models.CharField(default='12345', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='device',
            name='auth_token',
            field=models.ForeignKey(default='12346', on_delete=django.db.models.deletion.CASCADE, to='knox.AuthToken'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='moca.PaymentProfile'),
        ),
        migrations.AddField(
            model_name='payment',
            name='primary',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='status',
            field=models.CharField(choices=[('in-progress', 'In Progress'), ('not-started', 'Not Started'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('payment-failed', 'Payment Failed')], default='not-started', max_length=15),
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
        migrations.AlterField(
            model_name='note',
            name='appointment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='note', to='moca.Appointment'),
        ),
        migrations.AlterField(
            model_name='payment',
            name='name',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='noteimage',
            name='note',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='moca.Note'),
        ),
        migrations.AddField(
            model_name='issue',
            name='appointment',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='moca.Appointment'),
        ),
        migrations.AddField(
            model_name='issue',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='moca.Patient'),
        ),
        migrations.AddField(
            model_name='issue',
            name='therapist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='moca.Therapist'),
        ),
    ]
