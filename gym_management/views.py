from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, reverse, redirect, render

from django.http import HttpResponse, HttpResponseNotFound
from django.views import View

from django.urls import path, re_path, reverse_lazy

from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone

from django.contrib import messages

import django_tables2 as tables
from django_tables2 import RequestConfig
from django_tables2.export.export import TableExport
from django_tables2.export.views import ExportMixin



from .models import User, Invoice, MembershipType
from .tables import MemberTable



def seven_days_hence():
    return timezone.now() + timezone.timedelta(days=7)


MEMBERS_MAP = {
    'total_members':  User.objects.filter(is_staff=False, is_superuser=False),
    'active_members': User.objects.filter(is_staff=False, is_superuser=False).filter(
        membership_status=0, expires_at__gte=timezone.now()),
    'expired_members': User.objects.filter(is_staff=False, is_superuser=False).filter(
        membership_status=0, expires_at__lte=timezone.now()),
    'expiring_members': User.objects.filter(is_staff=False, is_superuser=False).filter(Q(membership_status=0) & Q(
        expires_at__lte=seven_days_hence()) & Q(expires_at__gte=timezone.now())),
}


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

    def get(self, request, member_type):
        try:

            if not member_type in MEMBERS_MAP.keys():
                raise Exception("Invalid Request")

            result = MEMBERS_MAP[member_type]
            print(member_type, result)
            # Give output as datatable

            return redirect(reverse_lazy('gym_management:stats_view'),)
        except Exception as e:
            messages.add_message(request, messages.WARNING, e)
            return redirect(reverse_lazy('gym_management:stats_view'))

            print(e)


class MembersTableView(ExportMixin,tables.SingleTableView):
    table_class = MemberTable
    queryset = MEMBERS_MAP['total_members']
    template_name = "stats/tables.html"
    paginator_class = tables.LazyPaginator
    paginate_by = 2


@staff_member_required
def members_table_view(request, member_type=None):
    if not member_type:
        member_type = 'total_members'
    if not member_type in MEMBERS_MAP.keys():
        member_type = 'total_members'

    table = MemberTable(MEMBERS_MAP[member_type])
    RequestConfig(request).configure(table)


    limit = request.GET.get('limit', 20)
    table.paginate(page=request.GET.get("page", 1),
                   per_page=limit if limit < 500 else 500)


    export_format = request.GET.get("_export", None)
    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response("table.{}".format(export_format))

    context = {
        "table": table,
    }
    for key,val in MEMBERS_MAP.items():
        context[key] = val
    return render(request, "stats/tables.html", context)
