# Generated by Django 2.1.10 on 2019-10-20 05:14

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.contrib.gis.geos.point
import django.contrib.postgres.fields
import django.contrib.postgres.fields.jsonb
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('gender', models.CharField(blank=True, choices=[('F', 'Female'), ('M', 'Male')], max_length=2, null=True)),
                ('date_of_birth', models.DateField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('type', models.CharField(choices=[('PA', 'Patient'), ('PT', 'Physical Therapist'), ('AG', 'Agent'), ('AD', 'Admin')], default='AG', max_length=2)),
                ('image', models.ImageField(blank=True, null=True, upload_to='users')),
                ('email', models.EmailField(max_length=254, null=True, unique=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('street', models.CharField(max_length=50)),
                ('apartment', models.CharField(max_length=50)),
                ('zip_code', models.CharField(max_length=5)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=2)),
                ('primary', models.BooleanField()),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('start_time_expected', models.DateTimeField(blank=True, null=True)),
                ('end_time_expected', models.DateTimeField(blank=True, null=True)),
                ('is_cancelled', models.BooleanField(default=False)),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='moca.Address')),
            ],
        ),
        migrations.CreateModel(
            name='AttachmentMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('url', models.FileField(upload_to='')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AwayDays',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField()),
                ('end_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Bank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('account_holder_name', models.CharField(max_length=20)),
                ('bank_name', models.CharField(max_length=20)),
                ('routing_number', models.CharField(max_length=20)),
                ('last_4', models.CharField(max_length=4)),
            ],
        ),
        migrations.CreateModel(
            name='Card',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('exp_year', models.CharField(max_length=4)),
                ('exp_month', models.CharField(max_length=2)),
                ('last_4', models.CharField(max_length=4)),
                ('brand', models.CharField(choices=[('Visa', 'Visa'), ('MasterCard', 'Mastercard'), ('American Express', 'Amex'), ('Discover', 'Discover'), ('JCB', 'JCB'), ('Diners Club', 'Diners Club'), ('UnionPay', 'UnionPay'), ('Unknown', 'Unknown')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Device',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=50)),
                ('type', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subjective', models.TextField(blank=True)),
                ('objective', models.TextField(blank=True)),
                ('treatment', models.TextField(blank=True)),
                ('assessment', models.TextField(blank=True)),
                ('diagnosis', models.TextField(blank=True)),
                ('files', django.contrib.postgres.fields.ArrayField(base_field=models.FileField(upload_to=''), size=None)),
                ('appointment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='moca.Appointment')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(choices=[('bank_account', 'Bank'), ('card', 'Card')], max_length=15)),
                ('token', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_customer_id', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('session_type', models.CharField(max_length=20)),
                ('price', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='RequestMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('options', django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moca.Conversation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ResponseMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('selection', models.IntegerField()),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moca.Conversation')),
                ('reply_to', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='moca.RequestMessage')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField()),
                ('comment', models.TextField(blank=True)),
                ('appointment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='moca.Appointment')),
            ],
        ),
        migrations.CreateModel(
            name='TextMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('text', models.TextField()),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moca.Conversation')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='patient', serialize=False, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Therapist',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='therapist', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('bio', models.CharField(blank=True, max_length=200, null=True)),
                ('cert_date', models.DateField(blank=True, null=True)),
                ('license_number', models.CharField(blank=True, max_length=50, null=True)),
                ('operation_radius', models.IntegerField(default=10)),
                ('qualifications', django.contrib.postgres.fields.jsonb.JSONField(default=dict)),
                ('status', models.CharField(choices=[('A', 'Available'), ('B', 'Busy')], default='A', max_length=100)),
                ('primary_location', django.contrib.gis.db.models.fields.PointField(default=django.contrib.gis.geos.point.Point(0, 0), srid=4326)),
                ('rating', models.FloatField(default=0)),
                ('review_count', models.IntegerField(default=0)),
                ('preferred_ailments', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), default=list, size=20)),
            ],
        ),
        migrations.AddField(
            model_name='textmessage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='responsemessage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='requestmessage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='paymentprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='device',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='conversation',
            name='participants',
            field=models.ManyToManyField(related_name='participants', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='card',
            name='payment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='moca.Payment'),
        ),
        migrations.AddField(
            model_name='card',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bank',
            name='payment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='moca.Payment'),
        ),
        migrations.AddField(
            model_name='bank',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='banks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='attachmentmessage',
            name='conversation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moca.Conversation'),
        ),
        migrations.AddField(
            model_name='attachmentmessage',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='address',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
        migrations.AddField(
            model_name='review',
            name='therapist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moca.Therapist'),
        ),
        migrations.AddField(
            model_name='price',
            name='therapist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tariffs', to='moca.Therapist'),
        ),
        migrations.AddField(
            model_name='awaydays',
            name='therapist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='awaydays', to='moca.Therapist'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moca.Patient'),
        ),
        migrations.AddField(
            model_name='appointment',
            name='therapist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moca.Therapist'),
        ),
    ]
