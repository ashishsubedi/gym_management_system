# Generated by Django 3.2 on 2021-04-07 17:46

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('name', models.CharField(max_length=255, verbose_name='Full Name')),
                ('phone_number', models.CharField(max_length=15, unique=True, verbose_name='Phone Number')),
                ('address', models.CharField(blank=True, max_length=100, null=True, verbose_name='Address')),
                ('rfid_code', models.CharField(blank=True, max_length=255, null=True, verbose_name='RFID Code')),
                ('membership_status', models.IntegerField(choices=[(0, 'ACTIVE'), (1, 'INACTIVE'), (2, 'BANNED'), (3, 'NONE')], default=1, verbose_name='Membership Status')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Joined Date')),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2021, 4, 7, 17, 46, 20, 280356, tzinfo=utc), verbose_name='Renewed Date')),
                ('expires_at', models.DateTimeField(verbose_name='Expiry Date')),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='MembershipType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('membership_type', models.CharField(max_length=40, verbose_name='Type')),
                ('price', models.FloatField(verbose_name='Price')),
                ('admission_fee', models.FloatField(verbose_name='Admission Fee')),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, verbose_name='Date')),
                ('price', models.FloatField(verbose_name='Price')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='membership_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='gym_management.membershiptype'),
        ),
    ]
