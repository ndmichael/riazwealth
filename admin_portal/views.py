from django.shortcuts import render


def admin_dashboard(request):
    context = {
        'title': 'Admin Portal'
    }
    return render(request, "admin_portal/admin_dashboard.html", context)
