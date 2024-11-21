from investments.models import UserInvestment

def get_total_profits(user):
    investments = UserInvestment.objects.filter(user=user)
    total_profits = sum([investment.total_profit for investment in investments])
    return total_profits
