from allauth.account.forms import SignupForm, LoginForm
from django import forms
from crispy_forms.layout import Layout, Submit, Row, Field
from crispy_forms.helper import FormHelper
from crispy_bootstrap5.bootstrap5 import FloatingField
from .models import  Profile
from referrals.models import Referral
from django.core.exceptions import ValidationError


class MyCustomSignupForm(SignupForm):

    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last name')
    terms_and_condition = forms.BooleanField(required=True)
    referral_code = forms.CharField(max_length=30, required=False)

    def __init__(self, *args, **kwargs):
        super().__init__( *args, **kwargs)

        self.fields['password1'].help_text = ""

        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                FloatingField("first_name", wrapper_class='col-md-6', css_class="row-fluid"),
                FloatingField("last_name", wrapper_class='col-md-6', css_class="row-fluid"),
            ),
            Row(
                FloatingField("email", wrapper_class='col-md-6', css_class="row-fluid"),
                FloatingField("username", wrapper_class='col-md-6', css_class="row-fluid"),
            ),
            Row(
                FloatingField("password1", wrapper_class='col-md-6', css_class="row-fluid"),
                FloatingField("password2", wrapper_class='col-md-6', css_class="row-fluid"),
            ),
            Row(
                FloatingField("referral_code", wrapper_class='col-12', css_class="row-fluid"),
            ),
            Row(
                Field("terms_and_condition", wrapper_class='col-md-6', css_class="form-check-input"),
            )                      
        )
    
    def clean_referral_code(self):
        referral_code = self.cleaned_data.get("referral_code")
        print(f"referral code: {referral_code}")
        if referral_code and not Profile.objects.filter(referral_code=referral_code.upper()).exists():
            raise forms.ValidationError("Invalid referral code.")
        return referral_code
    
    def save(self, request):
        # If there's a referral code, create a referral record
        referral_code = self.cleaned_data.get("referral_code").upper()
        # Call the parent save to create the user
        user = super().save(request)     

        if referral_code:
            try:
                referrer = Profile.objects.get(referral_code=referral_code)
                Referral.objects.create(referred_by=referrer.user, referred_to=user)

            except Exception as e:
                self.add_error(None, f"An error occurred while creating the referral: {e}")
                # Optional: Roll back user creation if referral creation is crucial
                user.delete() 
                # return None
                raise ValidationError(f"An error occurred while creating the referral: {e}") 
         
        return user
    
