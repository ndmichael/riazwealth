from allauth.account.adapter import DefaultAccountAdapter
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import resend
import os

resend.api_key = os.environ["RESEND_API_KEY"]

class AccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        subject = "".join(
            render_to_string(f"{template_prefix}_subject.txt", context).splitlines()
        )

        html = None
        try:
            html = render_to_string(f"{template_prefix}_message.html", context)
        except Exception:
            pass

        text = (
            render_to_string(f"{template_prefix}_message.txt", context)
            if html is None
            else strip_tags(html)
        )

        resend.Emails.send({
            "from": "Riazvest <noreply@riazvest.com>",
            "to": [email],
            "subject": subject,
            "html": html,
            "text": text,
        })