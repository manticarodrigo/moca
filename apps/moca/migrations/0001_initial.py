# Generated by Django 2.1.10 on 2019-12-03 00:26

from django.conf import settings
import django.contrib.gis.db.models.fields
import django.contrib.postgres.fields
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import moca.models.user.user


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
                ('email', moca.models.user.user.EmailField(max_length=254, null=True, unique=True)),
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
                ('apartment', models.CharField(blank=True, max_length=50)),
                ('zip_code', models.CharField(max_length=5)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=2)),
                ('primary', models.BooleanField()),
                ('location', django.contrib.gis.db.models.fields.PointField(srid=4326)),
                ('archive', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('start_time_manual', models.DateTimeField(blank=True, null=True)),
                ('end_time_manual', models.DateTimeField(blank=True, null=True)),
                ('status', models.CharField(choices=[('in-progress', 'In Progress'), ('not-started', 'Not Started'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('payment-failed', 'Payment Failed')], default='not-started', max_length=15)),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='moca.Address')),
            ],
        ),
        migrations.CreateModel(
            name='AppointmentCancellation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_processed', models.BooleanField(default=False)),
                ('type', models.CharField(choices=[('standard', 'Standard Cancellation Policy'), ('reschedule', 'Rescheduling'), ('weather', 'Cancellation Due to Weather'), ('emergency', 'Cancellation Due to an Emergency')], max_length=10)),
                ('cancellation_time', models.DateTimeField(auto_now_add=True)),
                ('appointment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='moca.Appointment')),
            ],
        ),
        migrations.CreateModel(
            name='AppointmentRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('accepted', 'Accepted'), ('rejected', 'Rejected'), ('pending', 'Pending'), ('cancelled', 'Cancelled')], default='pending', max_length=10)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now_add=True)),
                ('address', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='moca.Address')),
                ('appointment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='appointment', to='moca.Appointment')),
            ],
        ),
        migrations.CreateModel(
            name='AppointmentRequestMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('appointment_request', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='appointment_request', to='moca.AppointmentRequest')),
            ],
        ),
        migrations.CreateModel(
            name='AvailableArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('state', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='AwayPeriod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
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
                ('token', models.CharField(max_length=30)),
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
                ('token', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Certification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CertificationImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='certifications')),
                ('certification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='moca.Certification')),
            ],
        ),
        migrations.CreateModel(
            name='CompositeMessage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, null=True)),
                ('text', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CompositeMessageImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='messages')),
                ('message', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='moca.CompositeMessage')),
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
            ],
        ),
        migrations.CreateModel(
            name='EmailVerification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('EXPIRED', 'Expired'), ('PENDING', 'Pending'), ('VERIFIED', 'Verified')], default='PENDING', max_length=8)),
                ('created_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Injury',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='InjuryImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='injuries')),
                ('injury', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='moca.Injury')),
            ],
        ),
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('priority', models.CharField(choices=[('high', 'high'), ('normal', 'normal'), ('low', 'low')], default='normal', max_length=20)),
                ('description', models.TextField(null=True)),
                ('appointment', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='moca.Appointment')),
            ],
        ),
        migrations.CreateModel(
            name='LastViewed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moca.Conversation')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('type', models.CharField(choices=[('composite', 'Composite'), ('appointment-request', 'Appointment Request')], max_length=20)),
                ('conversation', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='moca.Conversation')),
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
                ('appointment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='note', to='moca.Appointment')),
            ],
        ),
        migrations.CreateModel(
            name='NoteImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='notes')),
                ('note', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='moca.Note')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('primary', models.BooleanField(default=False)),
                ('name', models.CharField(max_length=20, null=True)),
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
                ('session_type', models.CharField(choices=[('thirty', 'Thirty minutes'), ('fourtyfive', 'Fourty five minutes'), ('sixty', 'Sixty minutes'), ('evaluation', 'Evaluation')], max_length=20)),
                ('price', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('comment', models.TextField(blank=True)),
                ('appointment', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='moca.Appointment')),
            ],
        ),
        migrations.CreateModel(
            name='UnavailableArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('state', models.CharField(max_length=2)),
            ],
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
                ('is_verified', models.BooleanField(default=False)),
                ('operation_radius', models.IntegerField(default=10)),
                ('status', models.CharField(choices=[('A', 'Available'), ('B', 'Busy')], default='A', max_length=100)),
                ('primary_location', django.contrib.gis.db.models.fields.PointField(null=True, srid=4326)),
                ('rating', models.FloatField(default=0)),
                ('review_count', models.IntegerField(default=0)),
                ('preferred_ailments', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=20), default=list, size=20)),
            ],
        ),
        migrations.AddField(
            model_name='paymentprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='moca.PaymentProfile'),
        ),
        migrations.AddField(
            model_name='payment',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='lastviewed',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='emailverification',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='email_verification_tokens', to=settings.AUTH_USER_MODEL),
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
            model_name='compositemessage',
            name='message',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='moca.Message'),
        ),
        migrations.AddField(
            model_name='card',
            name='payment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='card', to='moca.Payment'),
        ),
        migrations.AddField(
            model_name='card',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cards', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='bank',
            name='payment',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='bank', to='moca.Payment'),
        ),
        migrations.AddField(
            model_name='bank',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='banks', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='appointmentrequestmessage',
            name='message',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='moca.Message'),
        ),
        migrations.AddField(
            model_name='appointmentcancellation',
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
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='moca.Patient'),
        ),
        migrations.AddField(
            model_name='review',
            name='therapist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='moca.Therapist'),
        ),
        migrations.AddField(
            model_name='price',
            name='therapist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='moca.Therapist'),
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
        migrations.AddField(
            model_name='injury',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='injuries', to='moca.Patient'),
        ),
        migrations.AddField(
            model_name='certification',
            name='therapist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='certifications', to='moca.Therapist'),
        ),
        migrations.AddField(
            model_name='awayperiod',
            name='therapist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='away_days', to='moca.Therapist'),
        ),
        migrations.AddField(
            model_name='appointmentrequest',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moca.Patient'),
        ),
        migrations.AddField(
            model_name='appointmentrequest',
            name='therapist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='moca.Therapist'),
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
        migrations.AlterUniqueTogether(
            name='price',
            unique_together={('therapist', 'session_type')},
        ),
    ]
