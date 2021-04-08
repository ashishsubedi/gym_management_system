from django.shortcuts import render
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, reverse, redirect


from django.urls import path, re_path,reverse_lazy

def reset_password(self,*args,**kwargs):
    pass
    user = self.request.user
    print(user)
    # if not self.has_change_permission(request):
    #     raise PermissionDenied()
    # user = get_object_or_404(self.model, pk=user_id)

    change_url = reverse('admin:auth_user_password_change', args=(user.id,))

    return change_url