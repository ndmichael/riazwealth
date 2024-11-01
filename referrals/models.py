from django.db import models
from accounts.models import CustomUser



class Referral(models.Model):
    referred_by = models.ForeignKey(CustomUser, related_name='referrer', on_delete=models.CASCADE)
    referred_to = models.ForeignKey(CustomUser, related_name='referred_user', on_delete=models.CASCADE)
    referral_date = models.DateTimeField(auto_now_add=True)
    referral_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.referred_by.username} referred {self.referred_to.username}"
