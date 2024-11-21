from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from investments.models import InvestmentPlan, UserInvestment
from withdrawals.models import WithdrawalRequest
from withdrawals.forms  import WithdrawalRequestForm

# Create your views here.

@login_required
def client_dashboard(request):
    user = request.user
    withdrawals = WithdrawalRequest.objects.filter(user=user)
    plans = InvestmentPlan.objects.all()
    user_investments = UserInvestment.objects.filter(user=user)

    withdrawals_amount = withdrawals.count()
    total_investments = user_investments.count()
    total_plans = plans.count()


    form = WithdrawalRequestForm()
    context ={
        "title": "client dashboard",
        "user": user,
        "plans": plans,
        "form": form,
        "withdrawals" : withdrawals,
        "user_investments": user_investments,
        "withdrawals_amount": withdrawals_amount,
        "total_investments": total_investments,
        "total_plans": total_plans
    }
    return render(request, "users/client_dashboard.html", context)

@login_required
def user_dashboard(request):

    if request.user.is_staff:
        return redirect('admindashboard')
    return redirect('clientdashboard')
