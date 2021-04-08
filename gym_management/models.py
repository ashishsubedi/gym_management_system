from django.db import models
from django.contrib.auth.models import (
    AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.utils import timezone
import re

CHOICES = (
    (0, 'ACTIVE'),
    (1, 'INACTIVE'),
    (2, 'BANNED'),
    (3, 'NONE'),
)


def one_month_hence():
    return timezone.now() + timezone.timedelta(days=30)


class MyUserManager(BaseUserManager):
    def create_user(self, name, phone_number, created_at, updated_at, expires_at, *args, **kwargs):
        """
        Creates and saves a User
        """
        if not phone_number:
            raise ValueError('Users must have a phone number')

        pattern = r'^(\+(01|1|977))?\d{7}(\d{3})?$'
        if not re.search(pattern.phone_number):
            raise ValueError('Enter a valid phone number')
        password = kwargs.pop('password', None)
        user = self.model(
            phone_number=phone_number,
            created_at=created_at,
            updated_at=updated_at,
            expires_at=expires_at,
            **kwargs
        )

        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, *args, **kwargs):
        """
        """
        user = self.model(
            phone_number=phone_number,

            **kwargs
        )
        user.set_password(password)

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    username = models.CharField(
        'Username', max_length=255, null=True, blank=True)

    # name = models.CharField('Full Name', max_length=255)
    password = models.CharField(
        "Password", max_length=255, null=True, blank=True)
    phone_number = models.CharField('Phone Number', max_length=15, unique=True)
    address = models.CharField(
        'Address', max_length=100, null=True, blank=True)
    rfid_code = models.CharField(
        'RFID Code', max_length=255, null=True, blank=True)

    membership_type = models.ForeignKey(
        'MembershipType', on_delete=models.CASCADE, related_name='members')

    membership_status = models.IntegerField(
        'Membership Status', choices=CHOICES, default=1)
    created_at = models.DateTimeField('Joined Date', auto_now_add=True)
    updated_at = models.DateTimeField('Renewed Date', default=timezone.now)
    expires_at = models.DateTimeField('Expiry Date', default=one_month_hence)


    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['membership_type', ]
    objects = MyUserManager()

    class Meta:
        verbose_name = "Member"

    def __str__(self):
        return f'{self.first_name}-{self.phone_number}'

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class MembershipType(models.Model):

    membership_type = models.CharField('Membership Type', max_length=40)
    price = models.FloatField('Price')
    admission_fee = models.FloatField('Admission Fee')

    def __str__(self):
        return f'{self.membership_type}'


class Invoice(models.Model):
    date = models.DateTimeField('Date', auto_now_add=True)
    amount = models.FloatField('Amount')
    user = models.ForeignKey(
        'User', on_delete=models.CASCADE, related_name='invoices')

    def __str__(self):
        return f'{self.date} by {self.user.first_name}'
