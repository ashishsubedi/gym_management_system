from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, reverse, redirect, render

from django.http import HttpResponse, HttpResponseNotFound
from django.views import View

from django.urls import path, re_path, reverse_lazy

from .models import User, Invoice, MembershipType
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone

from django.contrib import messages


def seven_days_hence():
    return timezone.now() + timezone.timedelta(days=7)


class StatsView(View):
    def get(self, request):
        total_members = User.objects.filter(is_staff=False, is_superuser=False)
        active_members = total_members.filter(
            membership_status=0, expires_at__gte=timezone.now())
        expired_members = total_members.filter(
            membership_status=0, expires_at__lte=timezone.now())
        expiring_members = total_members.filter(Q(membership_status=0) & Q(
            expires_at__lte=seven_days_hence()) & Q(expires_at__gte=timezone.now()))
        context = {
            'total_members': total_members,
            'active_members': active_members,
            'expired_members': expired_members,
            'expiring_members': expiring_members,
        }
        return render(request, 'stats/index.html', context=context)


@staff_member_required
def mark_all_expired_inactive(request):
    expired_members = User.objects.filter(
        is_staff=False, is_superuser=False).filter(Q(expires_at__lte=timezone.now()))
    expired_members.update(membership_status=1)

    messages.add_message(request, messages.SUCCESS,
                        'All expired users are deactivated.')

    return redirect(reverse_lazy('gym_management:stats_view'))


class StatsDetailView(View):
 
    MEMBERS_MAP = {
        'total_members':  User.objects.filter(is_staff=False, is_superuser=False),
        'active_members': User.objects.filter(is_staff=False, is_superuser=False).filter(
            membership_status=0, expires_at__gte=timezone.now()),
        'expired_members': User.objects.filter(is_staff=False, is_superuser=False).filter(
            membership_status=0, expires_at__lte=timezone.now()),
        'expiring_members': User.objects.filter(is_staff=False, is_superuser=False).filter(Q(membership_status=0) & Q(
            expires_at__lte=seven_days_hence()) & Q(expires_at__gte=timezone.now())),
    }

    def get(self, request, member_type):
        try:
            
            if not member_type in self.MEMBERS_MAP.keys():
                raise Exception("Invalid Request")

            result = self.MEMBERS_MAP[member_type]
            print(member_type,result)
            ##Give output as datatable

            return redirect(reverse_lazy('gym_management:stats_view'),)
        except Exception as e:
            messages.add_message(request, messages.WARNING, e)
            return redirect(reverse_lazy('gym_management:stats_view'))

            print(e)
