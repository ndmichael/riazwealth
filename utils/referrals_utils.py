from django.db.models import Count, Sum, Max, Q
from accounts.models import CustomUser
from referrals.models import Referral

def get_users_with_referrals(request):
    search_query = request.GET.get('user_q', '')

    users = CustomUser.objects.annotate(
        total_referrals=Count('referrer'),
        total_bonus=Sum('referrer__bonus'),
        highest_bonus=Max('referrer__bonus')
    ).order_by('-date_joined')  # Order by total bonus descending

    # Apply search filter if query exists
    if search_query:
        users = users.filter(Q(username__icontains=search_query) | Q(id__icontains=search_query))

    # Optimize active/inactive user count using filter inside Count
    user_counts = CustomUser.objects.aggregate(
        total_users=Count('id'),
        total_active_users=Count('id', filter=Q(is_active=True)),
        total_inactive_users=Count('id', filter=Q(is_active=False))
    )

    return users, user_counts['total_active_users'], user_counts['total_inactive_users']
