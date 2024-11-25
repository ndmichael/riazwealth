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


class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["bitcoin_wallet", "ethereum_wallet", "usdt_wallet"]
