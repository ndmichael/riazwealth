from django.db.models import Q
from django.core.paginator import Paginator
from withdrawals.models import WithdrawalRequest
from django.db.models import Q



def withdrawal_request_filter(request):
    # Get the active tab (default to 'pending')
    active_tab = request.GET.get('tab', 'pending')  # 'pending', 'rejected', 'successful'
    search_query = request.GET.get('q', '')

    # Filter withdrawals based on the active tab
    if active_tab == 'pending':
        withdrawals = WithdrawalRequest.objects.filter(status='pending').order_by("-created_at").order_by("-updated_at")
    elif active_tab == 'rejected':
        withdrawals = WithdrawalRequest.objects.filter(status='rejected').order_by("-created_at").order_by("-updated_at")
    elif active_tab == 'successful':
        withdrawals = WithdrawalRequest.objects.filter(status='successful').order_by("-created_at").order_by("-updated_at")
    else:
        withdrawals = WithdrawalRequest.objects.all().order_by("-created_at").order_by("-updated_at")  # Fallback for invalid tab values

    # Apply search filter if a query is provided
    if search_query:
        withdrawals = withdrawals.filter(
            Q(user__username__icontains=search_query) | Q(id__icontains=search_query)
        )

    # Paginate the filtered results
    paginator = Paginator(withdrawals, 10)  # 10 items per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return page_obj, active_tab, search_query
