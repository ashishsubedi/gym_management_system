from django.contrib import admin
from django.contrib.auth import get_user_model

from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .models import MembershipType, Invoice

User = get_user_model()


admin.site.site_header = 'Gym Management System'
admin.site.site_title = 'Strong Gym'
admin.site.index_title = 'Gym Management System'


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput,required=False)
  
    class Meta:
        model = User

        fields = (
            'name',
            'phone_number',
            'password1',
            'address',
            'rfid_code',
            'membership_type', 'membership_status',
            'updated_at', 'expires_at',
            'is_active', 'is_staff', 'is_admin', 'is_superuser'


        )


    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = (
            'name',
            'phone_number',
            'password',
            'address',
            'rfid_code',
            'membership_type', 'membership_status',
            'updated_at', 'expires_at',
            'is_active', 'is_staff', 'is_admin', 'is_superuser'

        )
    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    ordering = ('-created_at',)

    list_display = ('name', 'phone_number', 'membership_type',
                    'membership_status', 'created_at', 'updated_at', 'expires_at')
    add_fieldsets = (
        ('Basic Information', {
            'fields': (
                'name',
                'phone_number',
                'password1',

                'address',
                'rfid_code',
                ('membership_type', 'membership_status'),
                ('updated_at', 'expires_at')

            )
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': (

                ('is_active', 'is_staff', 'is_admin', 'is_superuser'),
                ('groups')
            )
        })
    )


admin.site.register(User, UserAdmin)
admin.site.register(MembershipType)
admin.site.register(Invoice)
