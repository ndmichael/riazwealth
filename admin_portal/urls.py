from django.urls import path
from .views import (
        admin_dashboard, 
        get_investment_details, 
        toggle_investment_status,
        confirm_withdrawal,
        accrue_profits_for_all_users
)

urlpatterns = [
    path('admin/dashboard', admin_dashboard, name='admindashboard'),
    path('admin/modal-content/<int:pk>/', get_investment_details, name='get_investment_details'),
    path('admin/investments/<int:investment_id>/toggle-status/', toggle_investment_status, name='get_investment_details'),
    path("admin/withdrawals/confirm/<int:withdrawal_id>/", confirm_withdrawal, name="confirm_withdrawal"),
    path('accrue_profits/', accrue_profits_for_all_users, name='accrue_profits_for_all_users'),
]