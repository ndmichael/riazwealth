from django.shortcuts import render
from django.db.models import Count, Q
from investments.models import InvestmentPlan, UserInvestment
from .forms import InvestmentFilterForm
from utils.filter_form import filter_investments


def admin_dashboard(request):

    investments = UserInvestment.objects.all()
    # active_investments = UserInvestment.objects.filter(status=True)
    # pending_investments = UserInvestment.objects.filter(status=False)
    # Aggregate counts in a single query
    investment_counts = UserInvestment.objects.aggregate(
        total_investments=Count('id'),
        total_active=Count('id', filter=Q(status=True)),
        total_pending=Count('id', filter=Q(status=False))
    )
    # total_investments = investments.count()
    # total_active = active_investments.count()
    # total_pending = pending_investments.count()
    plans = InvestmentPlan.objects.all()

    # active_tab = 'content-admin-investment'  # Default tab
    active_tab = request.GET.get('active_tab', 'content-admin-investment')
    filterForm =  InvestmentFilterForm(request.GET or None)

    # --- Active Tab Handling ---
    active_tab = request.GET.get('active_tab', active_tab)  

    if filterForm.is_valid():
        # Use cleaned data from the form
        ref_token = filterForm.cleaned_data.get('ref_token')
        status = filterForm.cleaned_data.get('status')

        # Check if at least one field has a value
        if ref_token or status:
            # Filter investments based on form input
            investments = filter_investments(ref_token, status)
        

    context = {
        'investments': investments,
        'plans': plans,
        'title': 'Admin Portal',
        "total_investments": investment_counts['total_investments'],
        'total_active': investment_counts['total_active'],
        'total_pending': investment_counts['total_pending'],


        # forms
        "filterForm": filterForm,
        "active_tab": active_tab
    }
    return render(request, "admin_portal/admin_dashboard.html", context)
