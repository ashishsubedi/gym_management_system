# Generated by Django 3.2 on 2021-04-08 08:21

from django.db import migrations, models
import gym_management.models


class Migration(migrations.Migration):

    dependencies = [
        ('gym_management', '0009_auto_20210408_1034'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invoice',
            name='price',
        ),
        migrations.RemoveField(
            model_name='user',
            name='is_admin',
        ),
        migrations.AddField(
            model_name='invoice',
            name='amount',
            field=models.FloatField(default=10, verbose_name='Amount'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='membershiptype',
            name='membership_type',
            field=models.CharField(max_length=40, verbose_name='Membership Type'),
        ),
        migrations.AlterField(
            model_name='user',
            name='expires_at',
            field=models.DateTimeField(default=gym_management.models.one_month_hence, verbose_name='Expiry Date'),
        ),
    ]
