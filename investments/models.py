from django.db import models
from accounts.models import CustomUser
from datetime import timedelta
from django.utils import timezone
from uuid import uuid4



payment_method = (
    ('bitcoin', 'BITCOIN'),
    ('ethereum', 'ETHEREUM'),
    ('usdt', 'USDT')
)

class InvestmentPlan(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    min_amount = models.DecimalField(max_digits=15, decimal_places=2)
    max_amount = models.DecimalField(max_digits=15, decimal_places=2)
    daily_profit_rate = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(default='planImg.png', upload_to='investment_plan_img/', blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name


class UserInvestment(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_investments')
    investment_plan = models.ForeignKey(InvestmentPlan, on_delete=models.CASCADE, related_name='investments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    daily_profit = models.DecimalField(max_digits=10, decimal_places=2)
    total_profit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    profit_accumulated = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_type = models.CharField(default='bitcoin', choices=payment_method, max_length=50)
    payment_proof = models.ImageField(upload_to='payment_proofs/', null=True, blank=True)
    payment_verified = models.BooleanField(default=False) 
    status = models.BooleanField(default=False) 
    next_accrual_date = models.DateField(blank=True, null=True)
    withdrawal_interval_days = models.PositiveIntegerField(default=7) 
    investment_date = models.DateTimeField(default=timezone.now)
    ref_token = models.CharField(
        null=False, 
        blank=False, 
        max_length=15, 
        unique=True, 
    )

    def __str__(self):
        return f"{self.investment_plan}, Amount: {self.amount} Status: {self.status} {self.user.get_full_name()}"
    

    def set_withdrawal_interval(self):
        """
        Set the withdrawal interval based on the amount invested.
        """
        if self.amount >= 10000:
            self.withdrawal_interval_days = 3
        elif self.amount >= 500:
            self.withdrawal_interval_days = 7
        else:
            self.withdrawal_interval_days = 14

        self.save()

    def calculate_next_withdrawal_date(self):
        """
        Calculate the next withdrawal date based on the investment start date and withdrawal interval.
        """
        if not self.payment_verified and not self.status:
            return None  # Withdrawal only allowed if payment is verified
        return self.investment_date + timedelta(days=self.withdrawal_interval_days)


    def calculate_daily_profit(self):
        """
        Calculate daily profit based on the investment plan, invested amount, and bonus tiers.
        """
        if self.status and self.payment_verified:
            # Base rate from the investment plan
            base_rate = self.investment_plan.daily_profit_rate / 100  # Convert to decimal

            # Determine bonus rate based on the invested amount
            if self.amount > 10000:
                bonus_rate = 0.01  # +1.0%
            elif self.amount > 5000:
                bonus_rate = 0.005  # +0.5%
            else:
                bonus_rate = 0.0  # No bonus

            # Calculate the total daily rate
            total_rate = base_rate + bonus_rate

            # Calculate daily profit
            daily_profit = self.amount * total_rate

            # Update accumulated and total profits
            self.profit_accumulated += daily_profit
            self.total_profit += daily_profit

            # Set the next accrual date
            self.next_accrual_date = timezone.now().date() + timedelta(days=1)

            # Save changes
            self.save()


    def accrue_profit(self):
        """
        Accrue daily profit if today matches the next accrual date.
        """
        today = timezone.now().date()
        if self.status and self.payment_verified and today >= self.next_accrual_date:
            self.calculate_daily_profit()


    def generate_unique_ref_token(self):
        while True:
            token = uuid4().hex[-10:].upper()  # Generate a new reference
            return token

    def save(self, *args, **kwargs):
        if not self.ref_token:  # Ensure reference is generated only if it's not set
            self.ref_token = self.generate_unique_ref_token()

        if self.payment_verified and not self.next_accrual_date:
            self.next_accrual_date = timezone.now().date() + timedelta(days=1)

        super().save(*args, **kwargs)  # Call the parent save method

    






# investment_plans = [
#     InvestmentPlan(
#         name='Stocks', 
#         description="""
#         Invest in a diversified portfolio of top-performing stocks across various industries.
#         Our stock investment plan aims to deliver a steady growth of 36% monthly.
#         Ideal for investors looking for moderate risk with the potential 
#         for significant returns through equity markets.
#         """,
#         min_amount=100,   
#         max_amount=5000000, 
#         daily_profit_rate=1.2
#     ),
#     InvestmentPlan(
#         name='Trade Bonds', 
#         description="""
#         Secure your wealth with trade bonds that offer a fixed return of 45% monthly profit. 
#         This plan is designed for investors seeking stability and predictable income streams from bond markets. 
#         Low risk and reliable performance make it an attractive option.
#         """,
#         min_amount=200, 
#         max_amount=5000000, 
#         daily_profit_rate=1.5
#     ),
#     InvestmentPlan(
#         name='Real Estate', 
#         description="""
#         Capitalize on the growth of the real estate market by investing in residential and commercial properties. 
#         With a 60% in a month, this plan offers a stable income and long-term appreciation. 
#         Ideal for investors seeking low risk and asset-backed security.
#         """,
#         min_amount=1000, 
#         max_amount=5000000, 
#         daily_profit_rate=2.0
#     ),
#     InvestmentPlan(
#         name='Gold and Silver', 
#         description="""
#         Invest in precious metals like gold and silver to preserve wealth and hedge against inflation. 
#         This plan offers a consistent monthly returns of 30%. 
#         Ideal for conservative investors focused on safety and wealth preservation.
#         """,
#         min_amount=500, 
#         max_amount=5000000, 
#         daily_profit_rate=1.0
#     ),
#     InvestmentPlan(
#         name='Bitcoin and Cryptocurrencies', 
#         description="""
#         Tap into the high-growth potential of the cryptocurrency market with this aggressive investment plan. 
#         With up to 70% profit monthly, 
#         this plan is perfect for investors willing to accept higher risk in exchange for potentially high returns.
#         """,
#         min_amount=100, 
#         max_amount=5000000, 
#         daily_profit_rate=2.5
#     ),
#     InvestmentPlan(
#         name='Oil and Gas', 
#         description="""
#         Profit from the booming energy sector by investing in oil and gas. 
#         Offering up to 54% profit monthly, this plan provides a balance of risk and reward, 
#         ideal for investors 
#         looking to capitalize on energy market trends and stable returns.
#         """,
#         min_amount=500, 
#         max_amount=5000000, 
#         daily_profit_rate=1.8
#     ),
#     InvestmentPlan(
#         name='AI and Web3', 
#         description="""
#         Invest in the future of technology by participating in artificial intelligence (AI) and Web3 projects. 
#         This high-growth plan offers a 66% monthly profits, ideal for tech-savvy investors seeking exposure to 
#         disruptive technologies and cutting-edge innovations.
#         """,
#         min_amount=1000, 
#         max_amount=5000000, 
#         daily_profit_rate=2.2
#     ),
# ]

# # Save the instances in bulk
# InvestmentPlan.objects.bulk_create(investment_plans)
