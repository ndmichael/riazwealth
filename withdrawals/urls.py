from django.urls import path
from .views import (admin_create_withdrawal, confirm_withdrawal)

urlpatterns = [
    path(
        "admin/withdrawals/create/",
        admin_create_withdrawal,
        name="admin_create_withdrawal"
    ),
    path(
        "admin/withdrawals/confirm/<int:withdrawal_id>/",
        confirm_withdrawal,
        name="confirm_withdrawal"
    ),
]