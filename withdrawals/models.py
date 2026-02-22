from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from investments.models import UserInvestment
from django.db.models import Max

# Status of the withdrawal request
STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]
PAYMENT_OPTIONS = [
    ('ethereum', 'Ethereum'),
    ('bitcoin', 'Bitcoin'),
    ('usdt', 'USDT'),
]
class WithdrawalRequest(models.Model):
    # User who made the withdrawal request
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    investment = models.ForeignKey(
        UserInvestment, 
        on_delete=models.CASCADE, 
        related_name='withdrawal_requests',
        null=True
    ) 
    
    # Amount requested for withdrawal
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    payment_option = models.CharField(_("payment options"), max_length=10, choices=PAYMENT_OPTIONS, default="usdt")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    receipt_number = models.CharField(
        max_length=30,
        unique=True,
        null=True,
        blank=True
    )

    approved_at = models.DateTimeField(
        null=True,
        blank=True
    )
    
    # Timestamp for when the request was created
    created_at = models.DateTimeField(_("request date"),auto_now_add=True)
    
    # Timestamp for when the request was updated
    updated_at = models.DateTimeField(_("updated date"),default=timezone.now)
    
    # Optional: Field for notes or comments by staff regarding the request
    notes = models.TextField(blank=True, null=True)

    def generate_receipt_number(self):
        year = timezone.now().year

        last_receipt = WithdrawalRequest.objects.filter(
            receipt_number__startswith=f"WR-{year}-"
        ).aggregate(
            Max("receipt_number")
        )["receipt_number__max"]

        if last_receipt:
            last_number = int(last_receipt.split("-")[-1])
            new_number = last_number + 1
        else:
            new_number = 1

        return f"WR-{year}-{str(new_number).zfill(6)}"

    def __str__(self):
        return f'{self.user.username} - {self.amount} ({self.status})'
    



