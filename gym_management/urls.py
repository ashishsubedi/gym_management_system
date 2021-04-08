
from django.urls import path

from .views import (
    StatsView,

    mark_all_expired_inactive,
)
from django.contrib.admin.views.decorators import staff_member_required

app_name = 'gym_management'

urlpatterns = [
    path('stats/', staff_member_required(StatsView.as_view()), name='stats_view'),
    path('make_inactive/',mark_all_expired_inactive,name='mark_expired_inactive')
]
