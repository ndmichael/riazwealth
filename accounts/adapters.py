from allauth.account.adapter import DefaultAccountAdapter
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import resend
import os

resend.api_key = os.environ["RESEND_API_KEY"]

class AccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        subject = render_to_string(
            f"{template_prefix}_subject.txt", context
        ).strip()

        html = render_to_string(
            f"{template_prefix}_message.html", context
        )

        text = strip_tags(html)

        resend.Emails.send({
            "from": "Riazvest <noreply@riazvest.com>",
            "to": email,
            "subject": subject,
            "html": html,
            "text": text,
        })