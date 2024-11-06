from django import forms
from .models import WithdrawalRequest

class WithdrawalRequestForm(forms.ModelForm):
    class Meta:
        model = WithdrawalRequest
        fields = ['amount', 'payment_option']  # Include payment_option in the form

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        # Add your validation logic here as before
        return amount
