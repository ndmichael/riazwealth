from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from investments.models import InvestmentPlan
from withdrawals.forms  import WithdrawalRequestForm

# Create your views here.

@login_required
def client_dashboard(request):
    plans = InvestmentPlan.objects.all()
    form = WithdrawalRequestForm()
    context ={
        "title": "client dashboard",
        "plans": plans,
        "form": form
    }
    return render(request, "users/client_dashboard.html", context)

@login_required
def user_dashboard(request):

    if request.user.is_staff:
        return redirect('admindashboard')
    return redirect('clientdashboard')
