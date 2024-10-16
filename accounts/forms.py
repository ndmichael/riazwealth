from allauth.account.forms import SignupForm, LoginForm
from django import forms
from crispy_forms.layout import Layout, Submit, Row, Field
from crispy_forms.helper import FormHelper
from crispy_bootstrap5.bootstrap5 import FloatingField


class MyCustomSignupForm(SignupForm):

    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last name')
    terms_and_condition = forms.BooleanField(required=True)


    def __init__(self, *args, **kwargs):
        super(MyCustomSignupForm, self).__init__(*args, **kwargs)

        self.fields['password1'].help_text = ""
        # self.fields['upliner'].disabled = True

        # super().__init__(*args, **kwargs)
        self.helper = FormHelper()
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
                Field("terms_and_condition", wrapper_class='col-md-12', css_class="form-check-input"),
            ),
            Submit('submit', 'Create Account', css_class="col-12 btn-lg btn-1 fw-bold")
                      
        )