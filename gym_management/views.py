from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, reverse, redirect,render

from django.http import HttpResponse, HttpResponseNotFound
from django.views import View

from django.urls import path, re_path,reverse_lazy

from .models import User,Invoice, MembershipType
from django.db.models import Q
from django.contrib.admin.views.decorators import staff_member_required


class StatsView(View):
    def get(self,request):
        members = User.objects.filter(~Q(membership_type__membership_type='admin'))
        print(members)
        context = {
            'members': members
        }
        return render(request,'stats/index.html', context=context)

