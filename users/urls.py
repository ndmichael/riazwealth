from django.urls import path
from .views import (
    user_dashboard,
    client_dashboard,
    mark_as_read
)




urlpatterns = [
    path('dashboard', client_dashboard , name="clientdashboard"),
    path('', user_dashboard, name="user_dashboard"),
    path('mark-as-read/', mark_as_read, name='mark_as_read'),
]