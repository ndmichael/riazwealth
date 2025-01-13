from investments.models import UserInvestment
from django.contrib.postgres.search import SearchVector


def filter_investments(ref_token="", status=""):
    # Logic to filter complaints by reference id
    investments = UserInvestment.objects.all()
    if ref_token:
        investments = UserInvestment.objects.filter(ref_token=ref_token)
    if status:
        investments = UserInvestment.objects.filter(status=status)

    return investments
