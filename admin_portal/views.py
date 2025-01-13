from django.shortcuts import render
from investments.models import InvestmentPlan, UserInvestment
from .forms import InvestmentFilterForm
from utils.filter_form import filter_investments


def admin_dashboard(request):

    investments = UserInvestment.objects.all()
    active_investments = UserInvestment.objects.filter(status=True)
    pending_investments = UserInvestment.objects.filter(status=False)
    total_investments = investments.count()
    total_active = active_investments.count()
    total_pending = pending_investments.count()
    plans = InvestmentPlan.objects.all()

    active_tab = 'content-admin-investment'  # Default tab
    filterForm =  InvestmentFilterForm(request.GET or None)
    if filterForm.is_valid():
        # Use cleaned data from the form
        ref_token = filterForm.cleaned_data.get('ref_token')
        status = filterForm.cleaned_data.get('status')
        print(f"ref token = {ref_token}")
        print(f"status = {status}")
        
        active_tab = request.GET.get('active_tab', 'content-admin-investment')
        investments = filter_investments(ref_token, status)
        

    context = {
        'investments': investments,
        'plans': plans,
        'title': 'Admin Portal',
        "total_investments": total_investments,
        'total_active': total_active,
        'total_pending': total_pending,

        # forms
        "filterForm": filterForm,
        "active_tab": active_tab
    }
    return render(request, "admin_portal/admin_dashboard.html", context)
