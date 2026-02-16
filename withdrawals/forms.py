from django import forms
from .models import WithdrawalRequest
from investments.models import UserInvestment
from crispy_forms.layout import Layout, Submit, Row
from crispy_forms.helper import FormHelper
from crispy_bootstrap5.bootstrap5 import FloatingField
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from accounts.models import CustomUser  # adjust import to your project

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
        amount = cleaned_data.get('amount')
        if amount is None:
            raise forms.ValidationError("Amount is required.")

        amount = Decimal(cleaned_data.get('amount'))

        # Fetch the investment object (assuming it's passed to the form)
        investment = next((i for i in self.investments if i.id == int(investment_id)), None)
        
        if not investment:
            raise forms.ValidationError("Invalid investment selected.")
        
        # Check if the amount exceeds the 20% limit
        max_withdrawable = investment.profit_accumulated * Decimal(0.2)
        if amount > max_withdrawable:
            raise forms.ValidationError(f"Amount exceeds the maximum withdrawable limit of {max_withdrawable:.2f}.")

        last_withdrawal_date = investment.get_last_withdrawal_date()
        eligible_date = last_withdrawal_date + timedelta(days=investment.withdrawal_interval_days)

        print(f"eligble date: {eligible_date} and timezone: {timezone.now()}")
        # Check if the investment is eligible for withdrawal
        if eligible_date.date() > timezone.now().date():
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
            Submit('withdrawal_form_submit', 'REQUEST WITHDRAWAL', css_class="col-12 btn-lg btn-1")
        )


# Withdrawal form for admin users only.
class AdminCreateWithdrawalForm(forms.Form):
    PAYMENT_OPTIONS = [
        ('usdt', 'USDT'),
        ('ethereum', 'Ethereum'),
        ('bitcoin', 'Bitcoin'),
    ]

    user = forms.ModelChoiceField(
        queryset=CustomUser.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    investment = forms.ModelChoiceField(
        queryset=UserInvestment.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    amount = forms.DecimalField(
        max_digits=15,
        decimal_places=2,
        min_value=Decimal("0.01"),
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'})
    )

    payment_option = forms.ChoiceField(
        choices=PAYMENT_OPTIONS,
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    notes = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3})
    )

    def __init__(self, *args, user_obj=None, **kwargs):
        super().__init__(*args, **kwargs)

        # If a user is selected, populate investments for that user only
        if user_obj:
            self.fields['investment'].queryset = UserInvestment.objects.filter(
                user=user_obj,
                status=True,
                payment_verified=True,
            )

    def clean(self):
        cleaned_data = super().clean()
        user = cleaned_data.get("user")
        investment = cleaned_data.get("investment")
        amount = cleaned_data.get("amount")

        if not user or not investment or amount is None:
            return cleaned_data

        # Ensure investment belongs to selected user
        if investment.user_id != user.id:
            raise forms.ValidationError("Selected investment does not belong to the selected user.")

        # Admin bypasses 20% and interval rules, BUT we still prevent negative balances
        if amount > investment.profit_accumulated:
            raise forms.ValidationError(
                f"Amount exceeds user's available accumulated profit (${investment.profit_accumulated:.2f})."
            )

        return cleaned_data


