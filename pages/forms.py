from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Row, Div
from crispy_bootstrap5.bootstrap5 import FloatingField, Field



class ContactForm(forms.Form):
    """Form for filtering and searching payment records"""

    your_name = forms.CharField(required=True)
    email = forms.EmailField( required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = True
        self.helper.form_tag = False

        self.helper.layout = Layout(
            Row(
                FloatingField("your_name", wrapper_class='col-md-6'),
                FloatingField("email", wrapper_class='col-md-6'),
                FloatingField("subject", wrapper_class='col-md-12'),
                FloatingField("message", rows=6, css_class='h-100 w-100'),
                Div(
                    Submit('submit', 'Contact Us', css_class='btn-lg btn-1'),
                )
                
            ),
        )