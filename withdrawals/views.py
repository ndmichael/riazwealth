from django.shortcuts import render, redirect
from .forms import WithdrawalRequestForm

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
