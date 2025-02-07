from django import forms
from .models import WithdrawalRequest
from investments.models import UserInvestment
from crispy_forms.layout import Layout, Submit, Row
from crispy_forms.helper import FormHelper
from crispy_bootstrap5.bootstrap5 import FloatingField
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

class WithdrawalRequestForm(forms.Form):
    AMOUNT_CHOICES = [
        ('', '---SELECT AMOUNT---'),
        (10, '$10'),
        (20, '$20'),
        (50, '$50'),
        (100, '$100'),
        (500, '$500'),
        (1000, '$1,000'),
        (2000, '$2,000'),
        (5000, '$5,000'),
        (10000, '$10,000')
    ]

    PAYMENT_OPTIONS = [
        ('usdt', 'USDT'),
        ('ethereum', 'Ethereum'),
        ('bitcoin', 'Bitcoin'),
    ]

    investment = forms.ChoiceField(
        choices=[],  # Populated dynamically in the view
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    amount = forms.ChoiceField(
        choices=AMOUNT_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    payment_option = forms.ChoiceField(
        choices=PAYMENT_OPTIONS, 
        widget=forms.Select(attrs={'class': 'form-select'})
    )


    def clean(self):
        cleaned_data = super().clean()
        investment_id = cleaned_data.get('investment')
        amount = Decimal(cleaned_data.get('amount'))

        # Fetch the investment object (assuming it's passed to the form)
        investment = next((i for i in self.investments if i.id == int(investment_id)), None)
        
        if not investment:
            raise forms.ValidationError("Invalid investment selected.")
        
        # Check if the amount exceeds the 20% limit
        max_withdrawable = investment.total_profit * Decimal(0.2)
        if amount > max_withdrawable:
            raise forms.ValidationError(f"Amount exceeds the maximum withdrawable limit of {max_withdrawable:.2f}.")

        last_withdrawal_date = investment.get_last_withdrawal_date()
        eligible_date = last_withdrawal_date + timedelta(days=investment.withdrawal_interval_days)

        # Check if the investment is eligible for withdrawal
        if eligible_date > timezone.now():
            raise forms.ValidationError(f"Withdrawal not allowed before {eligible_date.date()}.")

        return cleaned_data
    
    def __init__(self, *args, investments=None, **kwargs):
        super().__init__(*args, **kwargs)

        if investments:
            self.fields['investment'].choices = [
                    (i.id, f"Plan: {i.investment_plan.name}") for i in investments if i.status
                ]
        self.investments = investments
    
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                FloatingField("investment", wrapper_class='col-12', css_class="row-fluid"),
            ),
            Row(
                FloatingField("amount", wrapper_class='col-12', css_class="row-fluid"),
            ),
             Row(
                FloatingField("payment_option", wrapper_class='col-12', css_class="row-fluid"),
            ),
            Submit('submit', 'REQUEST WITHDRAWAL', css_class="col-12 btn-lg btn-1")
        )




