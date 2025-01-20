from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from investments.models import InvestmentPlan, UserInvestment
from withdrawals.models import WithdrawalRequest
from referrals.models import Referral
from withdrawals.forms  import WithdrawalRequestForm
from django.db.models import Sum, Q

from utils.total_investments_profit import get_user_total_profits, get_total_referral_bonus
from utils.process_form import handle_user_profile_form

# Create your views here.

@login_required
def client_dashboard(request):
    user = request.user
    withdrawals = WithdrawalRequest.objects.filter(user=user)
    plans = InvestmentPlan.objects.all()
    user_investments = UserInvestment.objects.filter(user=user)
    
    withdrawals_amount = withdrawals.aggregate(total=Sum('amount', default=0.00, filter=Q(status="approved")))['total']
    total_investments = user_investments.count()
    total_plans = plans.count()
    
    total_profits = get_user_total_profits(user)
    total_bonuses = get_total_referral_bonus(user)

    # Time for referrals
    referrals = Referral.objects.filter(referred_by=user)
    total_referrals = referrals.count()



    if request.POST:
        withdrawal_form = WithdrawalRequestForm(request.POST, investments=user_investments)
    else:
        withdrawal_form = WithdrawalRequestForm(investments=user_investments)

    user_form, profile_form = handle_user_profile_form(request)


    context ={
        "title": "client dashboard",
        "user": user,
        "plans": plans,
        "referrals": referrals,
        "withdrawal_form": withdrawal_form,
        "user_form": user_form,
        "profile_form": profile_form,
        "withdrawals" : withdrawals,
        "user_investments": user_investments,
        "withdrawals_amount": withdrawals_amount,
        "total_investments": total_investments,
        "total_plans": total_plans,
        "total_referrals": total_referrals,
        "total_profits": total_profits,
        "total_bonuses": total_bonuses,
    }
    return render(request, "users/client_dashboard.html", context)



@login_required
def user_dashboard(request):

    if request.user.is_staff:
        return redirect('admindashboard')
    return redirect('clientdashboard')
