from django.urls import path
from .views import (
    buy_investment
)




urlpatterns = [
    path('investments/payment/<str:package>', buy_investment, name="buy_investment")
]