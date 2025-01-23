from investments.models import UserInvestment
from referrals.models import Referral

def get_user_total_profits(user):
    investments = UserInvestment.objects.filter(user=user)
    total_profits = sum([investment.total_profit for investment in investments])
    return total_profits

def get_total_referral_bonus(user):
    referrals = Referral.objects.filter(referred_by=user)
    total_bonuses = sum([referral.referral_bonus for referral in referrals])
    return total_bonuses
