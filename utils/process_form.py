from django.contrib import messages
from users.forms import UserForm, ProfileForm
from investments.forms import MakePaymentForm, ConfirmPaymentForm
from django.shortcuts import redirect
from accounts.models import Profile
from investments.models import InvestmentPlan, UserInvestment


def handle_user_profile_form(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    user_form = UserForm(instance=user)
    profile_form = ProfileForm(instance=profile)
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            # Save the form
            user_form.save()
            profile_form.save()
            messages.success(request, "Your profile has been updated successfully!")

    return user_form, profile_form


def handle_investment_creation(request, investment_plan):
    if request.method == "POST":
        make_payment_form = MakePaymentForm(request.POST)
        confirm_payment_form = ConfirmPaymentForm(request.POST)

        if make_payment_form.is_valid() and confirm_payment_form.is_valid():
            # Extract form data
            amount = make_payment_form.cleaned_data['amount']
            payment_type = make_payment_form.cleaned_data['payment_type']
            confirm_payment = confirm_payment_form.cleaned_data['confirm_payment']
            payment_proof = confirm_payment_form.cleaned_data.get('send_proof_of_payment')

            if confirm_payment:
                # Create and save the investment
                investment = UserInvestment.objects.create(
                    user=request.user,  # Assuming user is logged in
                    investment_plan=investment_plan,
                    amount=amount,
                    daily_profit=0,  # Initial value, calculated later
                    payment_type=payment_type,
                    payment_proof=payment_proof,
                    payment_verified=False,  # Initially not verified
                    status=False,  # Initially inactive
                    next_accrual_date=None,  # Will be set after verification
                )
                investment.set_withdrawal_interval()  # Set withdrawal interval based on amount
                investment.save()
                messages.success(request, "Your investment has been created successfully! Awaiting approval.")
                return redirect('clientdashboard')  # Redirect to a summary or dashboard page
            else:
                messages.error(request, "You must confirm the payment to proceed.")
        else:
            make_payment_form = MakePaymentForm()
            confirm_payment_form = ConfirmPaymentForm()
    # Return forms in case of errors
    return make_payment_form, confirm_payment_form

