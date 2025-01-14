from django.urls import path
from .views import admin_dashboard, get_investment_details

urlpatterns = [
    path('admin/dashboard', admin_dashboard, name='admindashboard'),
    path('admin/modal-content/<int:pk>/', get_investment_details, name='get_investment_details'),
    
]