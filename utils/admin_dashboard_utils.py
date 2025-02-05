# utils.py
from django.db.models import Sum, Count
from investments.models import UserInvestment, CustomUser, InvestmentPlan
from withdrawals.models import WithdrawalRequest  # Assuming models are in the same app

def get_admin_dashboard_stats():
    """Calculates and returns aggregate data for the admin dashboard."""
    aggregate_data = UserInvestment.objects.aggregate(
        total_amount_invested=Sum('amount'),
        total_investments=Count('id'),
    )
    total_users = CustomUser.objects.count() or 0
    total_plans = InvestmentPlan.objects.count() or 0
    total_withdrawal_requests = WithdrawalRequest.objects.count() or 0
    total_approved_withdrawals_amount = WithdrawalRequest.objects.filter(
        status='approved'
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0 

    return {
        'total_investments': aggregate_data['total_investments'],
        'total_amount_invested': aggregate_data['total_amount_invested'],
        'total_users': total_users,
        'total_plans': total_plans,
        'total_withdrawal_requests': total_withdrawal_requests,
        'total_approved_withdrawals_amount': total_approved_withdrawals_amount,
    }

