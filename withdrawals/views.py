from django.shortcuts import render, redirect, get_object_or_404
from django.db import transaction
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from utils.general_news_utils import send_notification
from utils.send_withdrawal_email import send_withdrawal_email

from django.db.models import Sum
from investments.models import UserInvestment

from .forms import WithdrawalRequestForm, AdminCreateWithdrawalForm
from .models import WithdrawalRequest


def request_withdrawal(request):
    if request.method == 'POST':
        form = WithdrawalRequestForm(request.POST)
        if form.is_valid():
            withdrawal_request = form.save(commit=False)
            withdrawal_request.user = request.user  # Associate the request with the logged-in user
            withdrawal_request.save()
            return redirect('withdrawal_success')  # Redirect to a success page or another view
    else:
        form = WithdrawalRequestForm()

    return render(request, 'withdrawal/request_withdrawal.html', {'form': form})


@login_required
@staff_member_required
def admin_create_withdrawal(request):

    if request.method == "POST":
        form = AdminCreateWithdrawalForm(request.POST)

        if form.is_valid():
            user = form.cleaned_data["user"]
            investment = form.cleaned_data["investment"]
            amount = form.cleaned_data["amount"]
            payment_option = form.cleaned_data["payment_option"]
            notes = form.cleaned_data.get("notes")

            with transaction.atomic():

                # Deduct from accumulated profit only
                investment.profit_accumulated -= amount
                investment.save()

                withdrawal = WithdrawalRequest.objects.create(
                    user=user,
                    investment=investment,
                    amount=amount,
                    payment_option=payment_option,
                    status="approved",
                    notes=notes,
                )

            # In-app notification
            send_notification(
                user=user,
                notification_type="withdrawal",
                message=f"Withdrawal of ${amount:.2f} has been created and approved by admin."
            )

            # Email
            send_withdrawal_email(withdrawal)

            messages.success(request, "Withdrawal created successfully.")
            return redirect("admin_withdrawals_dashboard")

    else:
        form = AdminCreateWithdrawalForm()

    return render(request, "withdrawals/admin_create_withdrawal.html", {
        "form": form
    })


@login_required
@staff_member_required
def confirm_withdrawal(request, withdrawal_id):
    if request.method != "POST":
        return JsonResponse({"success": False, "message": "Invalid request method."})

    withdrawal = get_object_or_404(WithdrawalRequest, id=withdrawal_id)

    if withdrawal.status != "pending":
        return JsonResponse({"success": False, "message": "Only pending withdrawals can be confirmed."})

    investment = withdrawal.investment

    if not investment:
        return JsonResponse({"success": False, "message": "No linked investment found."})

    if withdrawal.amount > investment.profit_accumulated:
        return JsonResponse({"success": False, "message": "Insufficient funds to withdraw."})

    with transaction.atomic():
        # Deduct from accumulated profit ONLY
        investment.profit_accumulated -= withdrawal.amount
        investment.save(update_fields=["profit_accumulated"])

        # Approve withdrawal
        withdrawal.status = "approved"
        withdrawal.save()

    # Send in-app notification
    send_notification(
        user=withdrawal.user,
        notification_type="withdrawal",
        message=f"Withdrawal #{withdrawal.id} of ${withdrawal.amount:.2f} has been approved."
    )

    # Send email
    send_withdrawal_email(withdrawal)

    return JsonResponse({"success": True})


@staff_member_required
def admin_user_investments(request, user_id):
    qs = UserInvestment.objects.filter(
        user_id=user_id,
        status=True,
        payment_verified=True,
    ).select_related("investment_plan")

    investments = [
        {
            "id": inv.id,
            "plan": inv.investment_plan.name,
            "total_profit": f"{inv.total_profit:.2f}",
            "profit_accumulated": f"{inv.profit_accumulated:.2f}",
        }
        for inv in qs
    ]

    totals = qs.aggregate(
        total_profit_sum=Sum("total_profit"),
        accumulated_sum=Sum("profit_accumulated"),
    )

    return JsonResponse({
        "investments": investments,
        "totals": {
            "total_profit_sum": f"{(totals['total_profit_sum'] or 0):.2f}",
            "accumulated_sum": f"{(totals['accumulated_sum'] or 0):.2f}",
        }
    })