# accounts/adapters.py
from allauth.account.adapter import DefaultAccountAdapter
from django.template.loader import render_to_string
import resend, os

resend.api_key = os.environ["RESEND_API_KEY"]

class AccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        # determine which template to send
        if template_prefix.endswith("email_confirmation_signup"):
            template = "account/email/email_confirmation_signup_message.html"
            subject = render_to_string(
                "account/email/email_confirmation_signup_subject.txt",
                context,
            ).strip()
        else:
            return  # or handle other mails later

        html = render_to_string(template, context)

        resend.Emails.send({
            "from": "Riazvest <noreply@riazvest.com>",
            "to": email,
            "subject": subject,
            "html": html,
        })