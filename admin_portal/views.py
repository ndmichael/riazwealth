from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Count, Q
from investments.models import InvestmentPlan, UserInvestment
from withdrawals.models import WithdrawalRequest
from .forms import InvestmentFilterForm, InvestmentStatusForm
from django.contrib import messages
from utils.filter_form import filter_investments
from django.core.paginator import Paginator
from utils.withdrawals_utils import withdrawal_request_filter
# from utils.toggle_investment_status import toggle_investment_status

import logging

logger = logging.getLogger(__name__)


def admin_dashboard(request):
    
    investments = UserInvestment.objects.all().order_by("-investment_date")
    plans = InvestmentPlan.objects.all()    
    withdrawals =  WithdrawalRequest.objects.all().order_by("-created_at").order_by("updated_at")

    # Aggregate counts in a single query
    investment_counts = UserInvestment.objects.aggregate(
        total_investments=Count('id'),
        total_active=Count('id', filter=Q(status=True)),
        total_pending=Count('id', filter=Q(status=False))
    )

    # active_tab = 'content-admin-investment'  # Default tab
    active_tab = request.GET.get('active_tab', 'content-admin-investment')
    filterForm =  InvestmentFilterForm(request.GET or None)

    if filterForm.is_valid():
        # Use cleaned data from the form
        ref_token = filterForm.cleaned_data.get('ref_token')
        status = filterForm.cleaned_data.get('status')

        # Check if at least one field has a value
        if ref_token or status:
            # Filter investments based on form input
            investments = filter_investments(ref_token, status)

    
    # Get filtered and paginated data
    page_obj, active_tab, search_query = withdrawal_request_filter(request)
        

    context = {
        'investments': investments,
        'plans': plans,
        'withdrawals': withdrawals,
        
        'title': 'Admin Portal',
        "total_investments": investment_counts['total_investments'],
        'total_active': investment_counts['total_active'],
        'total_pending': investment_counts['total_pending'],


        # forms
        "filterForm": filterForm,
        "active_tab": active_tab,

        # handling withdrawals
        'withdrawals': page_obj,  
        'active_tab': active_tab, 
        'search_query': search_query, 
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


def toggle_investment_status(request, investment_id):
    print("===== ENTERING toggle_investment_status VIEW =====")  
    logger.info(f"Entering toggle_investment_status view. Request path: {request.path}, Method: {request.method}") 
    if request.method == "POST":
        action = request.POST.get("action")
        try:
            investment = UserInvestment.objects.get(id=investment_id)
            if action == 'activate':
                investment.status = True
                investment.payment_verified = True
                investment.calculate_daily_profit()
            else: 
                investment.status = False
                investment.payment_verified = False
            investment.save()
            logger.info("Exiting toggle_investment_status view.") # Log exit
            return JsonResponse({'status': 'success', 'message': 'Investment status updated.'})
        except UserInvestment.DoesNotExist:
            return JsonResponse({"success": False, "message": "Investment not found."}, status=404)
    return JsonResponse({"success": False, "message": "Invalid request."}, status=400)


@login_required
@csrf_exempt
def confirm_withdrawal(request, withdrawal_id):
    if request.method == "POST":
        withdrawal = get_object_or_404(WithdrawalRequest, id=withdrawal_id)
        
        if withdrawal.status != "pending":
            return JsonResponse({"success": False, "message": "Only pending withdrawals can be confirmed."})

        # Update the withdrawal status
        withdrawal.status = "successful"
        withdrawal.save()

        return JsonResponse({"success": True})
    return JsonResponse({"success": False, "message": "Invalid request method."})