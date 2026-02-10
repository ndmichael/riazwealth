# accounts/adapters.py
from allauth.account.adapter import DefaultAccountAdapter
from django.template.loader import render_to_string
import resend, os

resend.api_key = os.environ["RESEND_API_KEY"]

class AccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        if template_prefix.endswith("email_confirmation_signup"):
            subject = render_to_string(
                "account/email/email_confirmation_signup_subject.txt",
                context,
            ).strip()

            # 🔴 THIS IS THE FIX
            html = render_to_string("emails/auth/signup.html", context)

            resend.Emails.send({
                "from": "Riazvest <noreply@riazvest.com>",
                "to": email,
                "subject": subject,
                "html": html,
            })