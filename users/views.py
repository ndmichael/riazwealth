from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from investments.models import InvestmentPlan, UserInvestment
from withdrawals.models import WithdrawalRequest
from referrals.models import Referral
from notifications.models import GeneralNotification


from withdrawals.forms  import WithdrawalRequestForm
from django.db.models import Sum, Q
from decimal import Decimal

from utils.total_investments_profit import get_user_total_profits, get_total_referral_bonus
from utils.process_form import handle_user_profile_form

import logging

logger = logging.getLogger(__name__)

# Create your views here.

@login_required
def client_dashboard(request):
    user = request.user
    withdrawals = WithdrawalRequest.objects.filter(user=user)
    plans = InvestmentPlan.objects.all()
    user_investments = UserInvestment.objects.filter(user=user)
    general_news = GeneralNotification.objects.all().order_by("-created_at")[:5]
    
    withdrawals_amount = withdrawals.aggregate(total=Sum('amount', default=0.00, filter=Q(status="approved")))['total']
    total_investments = user_investments.count()
    total_plans = plans.count()
    
    total_profits = get_user_total_profits(user)
    total_bonuses = get_total_referral_bonus(user)

    # Time for referrals
    referrals = Referral.objects.filter(referred_by=user)
    total_referrals = referrals.count()


    if request.method == "POST":
        # Create the form and pass the investments
        withdrawal_form = WithdrawalRequestForm(request.POST, investments=user_investments)
        
        if withdrawal_form.is_valid():
            print(f"result: {withdrawal_form.cleaned_data}")

            # Get the selected investment ID from the form's cleaned data
            investment_id = withdrawal_form.cleaned_data['investment']
            payment_option = withdrawal_form.cleaned_data['payment_option']
            amount = withdrawal_form.cleaned_data['amount']

            print(f"amount: {amount}")

            
            try:
                # Fetch the actual UserInvestment instance corresponding to the selected ID
                investment = UserInvestment.objects.get(id=investment_id)

                WithdrawalRequest.objects.create(
                    investment=investment, 
                    amount=amount, 
                    user=request.user, 
                    payment_option=payment_option
                )

                # Show a success message
                messages.success(request, "Withdrawal request submitted successfully!")
                return redirect("clientdashboard")
            
            except UserInvestment.DoesNotExist:
                messages.error(request, "Invalid investment selected.")
                return redirect("clientdashboard")
        
        else:
            # Print form errors for debugging
            print("Form Errors:", withdrawal_form.errors)
    
    else:
        # If the request is GET, initialize the form with user investments
        withdrawal_form = WithdrawalRequestForm(investments=user_investments)

    user_form, profile_form = handle_user_profile_form(request)


    context ={
        "title": "client dashboard",
        "user": user,
        "plans": plans,
        "referrals": referrals,
        "general_news": general_news,
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
