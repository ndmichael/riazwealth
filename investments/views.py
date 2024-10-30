from django.shortcuts import render
from .models import InvestmentPlan
from .forms import MakePaymentForm, ConfirmPaymentForm



def buy_investment(request, plan: str):
    plan = InvestmentPlan.objects.get(name=plan)
    if request.method == "POST":
        paymentForm = MakePaymentForm(request.POST)
        confirmForm = ConfirmPaymentForm(request.POST)
        if paymentForm.is_valid() and confirmForm.is_valid():
            pass
    else:
        paymentForm = MakePaymentForm()
        confirmForm = ConfirmPaymentForm()

    context = {
        "title": "Buy investment",
        "plan": plan,
        "cp_form": confirmForm,
        "p_form" : paymentForm
    }
    return render(request, "investments/buy_investment.html", context)
