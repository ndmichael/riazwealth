from django.template.loader import render_to_string
from django.utils.html import strip_tags
import resend

def send_withdrawal_email(withdrawal):
    """
    Sends a withdrawal approved email. Ensure 'withdrawal' is already saved
    with amount and payment_option populated.
    """
    # Safety defaults
    amount = withdrawal.amount or 0
    payment_method = (withdrawal.payment_option or "N/A").upper()

    subject = f"Your Withdrawal #{withdrawal.id} is Being Processed"

    context = {
        "user": withdrawal.user,
        "withdrawal": withdrawal,
        "amount": amount,
        "payment_method": payment_method,
    }

    html = render_to_string("emails/transactions/withdrawal_approved.html", context)
    text = strip_tags(html)

    resend.Emails.send({
        "from": "Riazvest <noreply@riazvest.com>",
        "to": [withdrawal.user.email],
        "subject": subject,
        "html": html,
        "text": text,
    })