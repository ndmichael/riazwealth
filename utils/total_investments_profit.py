from investments.models import UserInvestment
from referrals.models import Referral

def get_user_total_profits(user):
    investments = UserInvestment.objects.filter(
        user=user, 
        status=True,
        payment_verified=True
    )
    total_profits = sum([investment.profit_accumulated for investment in investments])
    return total_profits

def get_total_referral_bonus(user):
    referrals = Referral.objects.filter(referred_by=user)
    total_bonuses = sum([referral.bonus for referral in referrals])
    return total_bonuses

def get_total_investment_amount(user):
    investments = UserInvestment.objects.filter(
        user=user, 
        status=True,
        payment_verified=True
    )
    investment_amount = sum([investment.amount for investment in investments])
    return investment_amount

def get_total_package_bonus(user):
    investments = UserInvestment.objects.filter(
        user=user, 
        status=True,
        payment_verified=True
    )
    total_profits = sum([investment.package_bonus_amount for investment in investments])
    return total_profits

