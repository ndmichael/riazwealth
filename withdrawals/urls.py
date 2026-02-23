from django.urls import path
from .views import (
    admin_create_withdrawal, 
    confirm_withdrawal, 
    admin_user_investments, 
    withdrawal_receipt
)

urlpatterns = [
    path(
        "admin/create/",
        admin_create_withdrawal,
        name="admin_create_withdrawal"
    ),
    path(
        "admin/confirm/<int:withdrawal_id>/",
        confirm_withdrawal,
        name="confirm_withdrawal"
    ),
     path("admin/user-investments/<int:user_id>/", 
          admin_user_investments, 
          name="admin_user_investments"
    ),
    path(
        "receipt/<int:withdrawal_id>/",
        withdrawal_receipt,
        name="withdrawal_receipt"
    )
]