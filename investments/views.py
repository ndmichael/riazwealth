from django.shortcuts import render
from .forms import MakePaymentForm, ConfirmPaymentForm



def buy_investment(request, package: str):
    paymentForm = MakePaymentForm(request.POST)
    confirmForm = ConfirmPaymentForm(request.POST)
    context = {
        "title": "Buy investment",
        "cp_form": confirmForm,
        "p_form" : paymentForm
    }
    return render(request, "investments/buy_investment.html", context)
