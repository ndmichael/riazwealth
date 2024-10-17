from django.db import models
from accounts.models import CustomUser
from datetime import timedelta


class InvestmentPlan(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    roi_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    duration_days = models.PositiveIntegerField()
    min_amount = models.DecimalField(max_digits=10, decimal_places=2)
    max_amount = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserInvestment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_investments')
    investment_plan = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE, related_name='investments')
    amount_invested = models.DecimalField(max_digits=10, decimal_places=2)
    daily_profit = models.DecimalField(max_digits=10, decimal_places=2)
    total_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit_accumulated = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_proof = models.ImageField(upload_to='payment_proofs/', null=True, blank=True)
    payment_verified = models.BooleanField(default=False) 
    investment_status = models.BooleanField(default=False) 
    next_accrual_date = models.DateField()
    withdrawal_interval_days = models.PositiveIntegerField(default=7) 
    investment_date = models.DateTimeField(auto_now_add=True)
    

    def set_withdrawal_interval(self):
        """
        Set the withdrawal interval based on the amount invested.
        """
        if self.amount_invested >= 10000:
            self.withdrawal_interval_days = 3
        else:
            self.withdrawal_interval_days = 7

        self.save()

    def calculate_next_withdrawal_date(self):
        pass

    def calculate_daily_profit(self):
        # Logic to calculate daily profit and add to total_profit
        pass

    def accrue_profit(self):
        pass

