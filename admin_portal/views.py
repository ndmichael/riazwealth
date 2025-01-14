from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count, Q
from investments.models import InvestmentPlan, UserInvestment
from .forms import InvestmentFilterForm, InvestmentStatusForm
from django.contrib import messages
from utils.filter_form import filter_investments
from utils.toggle_investment_status import toggle_investment_status


def admin_dashboard(request):

    investments = UserInvestment.objects.all()

    # Aggregate counts in a single query
    investment_counts = UserInvestment.objects.aggregate(
        total_investments=Count('id'),
        total_active=Count('id', filter=Q(status=True)),
        total_pending=Count('id', filter=Q(status=False))
    )
    plans = InvestmentPlan.objects.all()

    if request.method == 'POST':
        toggle_form = InvestmentStatusForm(request.POST)
        if toggle_form.is_valid():
            investment_id = toggle_form.cleaned_data['investment_id']
            action = toggle_form.cleaned_data['action']
            
            print(f"action: {action},  id: {investment_id}")

            # Call the utility function
            message = toggle_investment_status(investment_id, action)
            messages.info(request, message)
            return redirect('admindashboard')  # Redirect to avoid form resubmission
    else:
        toggle_form = InvestmentStatusForm()
        

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
        "active_tab": active_tab,
        "toggle_form": toggle_form
    }
    return render(request, "admin_portal/admin_dashboard.html", context)


def get_investment_details(request, pk):
    print(f"{pk} : {type(pk)}")
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest' and request.method == 'GET':
        investment = get_object_or_404(UserInvestment, id=pk)
        data = {
            "ref_token":  investment.ref_token,
            "name": investment.investment_plan.name,
            "amount": investment.amount,
            "plan_name": investment.investment_plan.name,
            "payment_type": investment.payment_type,
            "user": investment.user.username,
            "payment_verified": investment.payment_verified,
            "daily_profit": investment.daily_profit,
            "accrual_date": investment.next_accrual_date,
            "date": investment.investment_date 

        }
        return JsonResponse(data)
    return JsonResponse({'error': 'Invalid request'}, status=400)
