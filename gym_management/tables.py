import django_tables2 as tables
from .models import User,MembershipType,Invoice

class MemberTable(tables.Table):
    class Meta:
        model = User
        template_name = "django_tables2/bootstrap4.html"
        attrs = {
            'class':'table table-bordered',
        }
        fields = ("first_name",'last_name','phone_number','membership_type','membership_status','created_at','updated_at','expires_at' )

