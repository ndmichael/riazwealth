from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def user_dashboard(request):
    if request.user.is_staff:
        return redirect('admindashboard')
    return redirect('clientdashboard', username=request.user.username)
