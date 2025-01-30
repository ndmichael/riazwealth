from django import forms
from .models import GeneralNotification
from crispy_forms.layout import Layout, Submit, Row, Field
from crispy_forms.helper import FormHelper
from crispy_bootstrap5.bootstrap5 import FloatingField

class GeneralNewsForm(forms.ModelForm):
    """Form for admins to create general news/announcements"""
    class Meta:
        model = GeneralNotification
        fields = ['title', 'message']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.disable_csrf = False
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(
                FloatingField("title", wrapper_class='col-md-12'),
                FloatingField("message", wrapper_class='col-md-12'),
            ),
        )