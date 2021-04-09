
from django.urls import path

from .views import (
    StatsView,
    StatsDetailView,
    MembersTableView,
    members_table_view,
    invoice_table_view,
    mark_all_expired_inactive,
)
from django.contrib.admin.views.decorators import staff_member_required

app_name = 'gym_management'

urlpatterns = [
    path('stats/', staff_member_required(StatsView.as_view()), name='stats_view'),
    path('stats/<str:member_type>/', staff_member_required(StatsDetailView.as_view()), name='stats_detail_view'),
    path('stats/table/show/', staff_member_required(MembersTableView.as_view()), name='stats_table_member_view'),
    path('stats/table/<str:member_type>/', members_table_view, name='stats_table_view'),
    path('stats/table/<int:phone_number>/invoice', invoice_table_view, name='invoice_table_view'),

    path('make_inactive/',mark_all_expired_inactive,name='mark_expired_inactive')
]
