from django.db import models
from django.utils import timezone
from accounts.models import CustomUser



class Referral(models.Model):
    referred_by = models.ForeignKey(CustomUser, related_name='referrer', on_delete=models.CASCADE)
    referred_to = models.ForeignKey(CustomUser, related_name='referred_user', on_delete=models.CASCADE)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    bonus_status = models.BooleanField(default=False) 
    created_at = models.DateTimeField(default=timezone.now)
    used_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.referred_by.username} referred {self.referred_to.username}"
