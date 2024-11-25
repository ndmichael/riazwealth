from django.contrib import messages
from users.forms import UserForm
from django.shortcuts import get_object_or_404
from accounts.models import Profile


def handle_user_form(request):
    user = request.user
    profile = Profile.objects.get_or_create(user=user)

    user_form = UserForm(instance=user)
    
    if request.method == "POST":
        if user_form.is_valid():
            # Save the form
            user_form.save()
            messages.success(request, "Your withdrawal request was submitted successfully!")

    return user_form
