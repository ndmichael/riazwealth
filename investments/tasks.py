from celery import shared_task
from django.utils import timezone
from .models import UserInvestment
from django.db.models import Q
from utils.general_news_utils import send_notification


@shared_task
def accrue_profits():
    today = timezone.now().date()
    investments = UserInvestment.objects.filter(
        status=True, 
        payment_verified=True,
        next_accrual_date__lte=today
    ).filter(
        Q(last_accrual_date__lt=today) | Q(last_accrual_date__isnull=True)  
    )

    count = 0  # Track successful accruals
    
    for investment in investments:
        investment.accrue_profit()
        # Send a notification
        send_notification(
            user=investment.user,
            notification_type="investment",
            message=f"""${investment.daily_profit} has been accrue to your wallet."""
        )
        count += 1  # Increment success count
    
    return f"Accrued profits for {count} users"
