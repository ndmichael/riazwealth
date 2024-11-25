from allauth.account.forms import SignupForm, LoginForm
from django import forms
from crispy_forms.layout import Layout, Submit, Row, Field
from crispy_forms.helper import FormHelper
from crispy_bootstrap5.bootstrap5 import FloatingField
from accounts.models import CustomUser, Profile



class UserForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ["username", "email", "first_name", "last_name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                FloatingField("username", wrapper_class='col-md-6'),
                FloatingField("email", wrapper_class='col-md-6'),
                FloatingField("first_name", wrapper_class='col-md-6'),
                FloatingField("last_name", wrapper_class='col-md-6'),
            ),
        )


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["bitcoin_wallet", "ethereum_wallet", "usdt_wallet"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                FloatingField("bitcoin_wallet", wrapper_class='col-md-12'),
                FloatingField("ethereum_wallet", wrapper_class='col-md-12'),
                FloatingField("usdt_wallet", wrapper_class='col-md-12'),
            ),
        )
