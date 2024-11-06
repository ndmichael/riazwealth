from django import forms
from .models import WithdrawalRequest
from crispy_forms.layout import Layout, Submit, Row
from crispy_forms.helper import FormHelper
from crispy_bootstrap5.bootstrap5 import FloatingField

class WithdrawalRequestForm(forms.ModelForm):
    class Meta:
        model = WithdrawalRequest
        fields = ['amount', 'payment_option']  # Include payment_option in the form

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        # Add your validation logic here as before
        return amount
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        # super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                FloatingField("amount", wrapper_class='col-12', css_class="row-fluid"),
            ),
             Row(
                FloatingField("payment_option", wrapper_class='col-12', css_class="row-fluid"),
            ),
            Submit('submit', 'REQUEST WITHDRAW', css_class="col-12 btn-lg btn-1")
        )