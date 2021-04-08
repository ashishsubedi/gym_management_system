from django.contrib import admin
from django.contrib.auth import get_user_model

from django import forms
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import (
    ReadOnlyPasswordHashField,
    PasswordResetForm
)

from django.utils.text import format_lazy
from django.urls import reverse_lazy, path


from .models import MembershipType, Invoice

from daterangefilter.filters import DateRangeFilter, FutureDateRangeFilter, PastDateRangeFilter

    
User = get_user_model()


admin.site.site_header = 'Gym Management System'
admin.site.site_title = 'Strong Gym'
admin.site.index_title = 'Gym Management System'


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password = forms.CharField(
        label='Password', widget=forms.PasswordInput, required=False)

    class Meta:
        model = User

        fields = (
            'first_name',
            'last_name',
            'phone_number',
            'password',
            'address',
            'rfid_code',
            'membership_type', 'membership_status',
            'updated_at', 'expires_at',
            'is_active', 'is_staff',  'is_superuser'


        )

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


# class UserChangeForm(forms.ModelForm):
#     """A form for updating users. Includes all the fields on
#     the user, but replaces the password field with admin's
#     password hash display field.
#     """
#     password = ReadOnlyPasswordHashField()

#     class Meta:
#         model = User
#         fields = (
#             'name',
#             'phone_number',
#             'password',
#             'address',
#             'rfid_code',
#             'membership_type', 'membership_status',
#             'updated_at', 'expires_at',
#             'is_active', 'is_staff', 'is_superuser'

#         )

#     def clean_password(self):
#         return self.initial["password"]


class InvoiceInline(admin.StackedInline):
    model = Invoice
    extra = 1
    readonly_fields = ('date', 'user')
    fields = ('amount',)


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    ordering = ('-created_at',)
    save_as = True
    save_on_top = True
    inlines = (InvoiceInline,)
    # date_hierarchy = 'expires_at'
    list_filter = (

        'membership_type__membership_type', 'membership_status',
        ('created_at', PastDateRangeFilter),
        ('updated_at', DateRangeFilter),
        ('expires_at', FutureDateRangeFilter),
    )

    list_display = ('phone_number', 'first_name', 'last_name', 'membership_type',
                    'membership_status', 'created_at', 'updated_at', 'expires_at')
    fieldsets = (
        ('Basic Information', {
            'fields': (
                ('first_name', 'last_name'),
                'phone_number',

                'password',
                'address',
                'rfid_code',
                ('membership_type', 'membership_status'),
                ('updated_at', 'expires_at')

            )
        }),
        ('Advanced', {
            'classes': ('collapse',),
            'fields': (

                ('is_active'), 
                ('is_staff', 'is_superuser'),
                ('groups')
            )
        })
    )
    add_fieldsets = fieldsets


admin.site.register(User, UserAdmin)
admin.site.register(MembershipType)

class InvoiceAdmin(admin.ModelAdmin):
    model = Invoice
    list_display = ('date', 'user','amount')
    ordering = ('-date',)


admin.site.register(Invoice, InvoiceAdmin)
