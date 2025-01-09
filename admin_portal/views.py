from django.shortcuts import render
from investments.models import InvestmentPlan, UserInvestment


def admin_dashboard(request):
    investments = UserInvestment.objects.all()
    context = {
        'investments': investments,
        'title': 'Admin Portal'
    }
    return render(request, "admin_portal/admin_dashboard.html", context)
