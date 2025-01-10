from django.shortcuts import render, redirect
from .models import InvestmentPlan
from .forms import MakePaymentForm, ConfirmPaymentForm
from django.contrib import messages
from utils.process_form import handle_investment_creation



def buy_investment(request, plan: str):
    # Get the investment plan by name
    try:
        investment_plan = InvestmentPlan.objects.get(name=plan)
    except InvestmentPlan.DoesNotExist:
        messages.error(request, "The specified investment plan does not exist.")
        return redirect('create_investment')
    
    if request.method == 'POST':
        result = handle_investment_creation(request, investment_plan)
        if not isinstance(result, tuple):
            # If the result is not a tuple, it's a redirect
            return result
        make_payment_form, confirm_payment_form = result
    else:
        make_payment_form = MakePaymentForm()
        confirm_payment_form = ConfirmPaymentForm()

    context = {
        "title": "Buy investment",
        "plan": investment_plan,
        "cp_form": confirm_payment_form,
        "p_form" :  make_payment_form
    }
    return render(request, "investments/buy_investment.html", context)
