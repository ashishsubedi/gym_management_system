
from django.urls import path

from .views import (
    StatsView,
    StatsDetailView,

    mark_all_expired_inactive,
)
from django.contrib.admin.views.decorators import staff_member_required

app_name = 'gym_management'

urlpatterns = [
    path('stats/', staff_member_required(StatsView.as_view()), name='stats_view'),
    path('stats/<str:member_type>', staff_member_required(StatsDetailView.as_view()), name='stats_detail_view'),

    path('make_inactive/',mark_all_expired_inactive,name='mark_expired_inactive')
]
