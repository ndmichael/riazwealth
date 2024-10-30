from django import forms



payment_method = (
    ('', 'SELECT PAYMENT METHOD'),
    ('bitcoin', 'BITCOIN'),
    ('ethereum', 'ETHEREUM'),
    ('usdt', 'USDT')
)
class MakePaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2, widget=forms.NumberInput({'class': 'form-control-lg'}))
    payment_type = forms.ChoiceField(choices=payment_method, widget=forms.Select({'class': 'form-select form-select-lg'}))


class ConfirmPaymentForm(forms.Form):
    confirm_payment = forms.BooleanField()
    send_proof_of_payment = forms.ImageField(required=False)