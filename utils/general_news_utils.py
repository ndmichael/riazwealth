from  notifications.forms import GeneralNewsForm
from django.contrib import messages
from django.shortcuts import redirect
from notifications.models import UserNotification


def post_general_news(request):
    if request.method == 'POST':
        form = GeneralNewsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "News posted successfully!")
            return redirect("admin_dashboard")
        return form
    return GeneralNewsForm()


def send_notification(user, notification_type, message):
    UserNotification.objects.create(user=user, notification_type=notification_type, message=message)

