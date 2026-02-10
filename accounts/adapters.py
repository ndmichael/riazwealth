# accounts/adapters.py
from allauth.account.adapter import DefaultAccountAdapter
import threading

class AccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        threading.Thread(
            target=super().send_mail,
            args=(template_prefix, email, context),
            daemon=True,
        ).start()