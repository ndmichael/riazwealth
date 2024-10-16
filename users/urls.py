from django.urls import path
from .views import (
    user_dashboard,
    client_dashboard,
)




urlpatterns = [
    path('dashboard', client_dashboard , name="clientdashboard"),
    path('', user_dashboard, name="user_dashboard"),
]