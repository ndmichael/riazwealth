from django.urls import path
from .views import (
    user_dashboard
)




urlpatterns = [
    # path('dashboard/', profile , name="clientdashboard"),
    path('', user_dashboard, name="user_dashboard"),
]