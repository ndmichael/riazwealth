# utils.py
from django.shortcuts import get_object_or_404
from django.contrib import messages
from investments.models import UserInvestment

def toggle_investment_status(investment_id, action):
    """
    Toggle the activation status of an investment.
    
    :param investment_id: ID of the investment to be toggled
    :param action: Action to perform ('activate' or 'deactivate')
    :return: Success message or error message
    """
    # Get the investment or raise a 404 error if not found
    investment = get_object_or_404(UserInvestment, id=investment_id)

    print(f"action: {action},  id: {investment_id}")

    # Perform the action
    if action == 'activate':
        if investment.payment_verified:
            investment.status = True
            investment.save()
            return f"Investment {investment.ref_token} has been activated successfully."
        else:
            return "Investment cannot be activated as the payment is not verified."
    elif action == 'deactivate':
        investment.status = False
        investment.save()
        return f"Investment {investment.ref_token} has been deactivated successfully."
    else:
        return "Invalid action specified."
