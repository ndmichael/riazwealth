from django.contrib import messages
from users.forms import UserForm, ProfileForm
from django.shortcuts import get_object_or_404
from accounts.models import Profile


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
            messages.success(request, "Your withdrawal request was submitted successfully!")

    return user_form, profile_form
