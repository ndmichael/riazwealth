from django import forms
from investments.models import UserInvestment
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Div, Row
from crispy_bootstrap5.bootstrap5 import FloatingField


class  InvestmentStatusForm(forms.Form):
    """Update Investment Form"""
    action = forms.ChoiceField(
        choices=[('activate', 'Activate'), ('deactivate', 'Deactivate')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'})
    )

class InvestmentFilterForm(forms.Form):
    """Form to filter complaint records."""
    STATUS  =( 
        ('', '----'),
        (True, 'ACTIVE'),
        (False, 'PENDING')
    )
    ref_token = forms.CharField(required=False)
    status = forms.ChoiceField(choices=STATUS, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.layout = Layout(
            Row(
                FloatingField("ref_token", wrapper_class='col-md-4'),
                FloatingField("status", wrapper_class='col-md-4'),
                Div(
                    Submit('submit', 'filter',  css_class="col-12 col-md-8 btn-lg btn-primary"), 
                    css_class='col-md-4',        
                )    
            ),
        )