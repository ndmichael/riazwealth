from django.db.models import Count, Sum, Max
from accounts.models import CustomUser
from referrals.models import Referral

def get_users_with_referrals():
    user = CustomUser.objects.annotate(
        total_referrals=Count('referrer'),
        total_bonus=Sum('referrer__bonus'),
        highest_bonus=Max('referrer__bonus')
    ).order_by('-date_joined')  # Order by total bonus descending
    return user
