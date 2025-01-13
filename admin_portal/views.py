from django.shortcuts import render
from investments.models import InvestmentPlan, UserInvestment


def admin_dashboard(request):
    investments = UserInvestment.objects.all()
    active_investments = UserInvestment.objects.filter(status=True)
    pending_investments = UserInvestment.objects.filter(status=False)
    total_investments = investments.count()
    total_active = active_investments.count()
    total_pending = pending_investments.count()
    plans = InvestmentPlan.objects.all()
    context = {
        'investments': investments,
        'plans': plans,
        'title': 'Admin Portal',
        "total_investments": total_investments,
        'total_active': total_active,
        'total_pending': total_pending
    }
    return render(request, "admin_portal/admin_dashboard.html", context)
