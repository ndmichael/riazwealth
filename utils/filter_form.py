from investments.models import UserInvestment
from django.contrib.postgres.search import SearchVector


def filter_investments(ref_token="", status=""):
    # Logic to filter complaints by reference id
    if ref_token and ref_token != '':
        investments = UserInvestment.objects.annotate(search=SearchVector('reference_id'),).filter(search__icontains=ref_token)

    # Logic to filter complaints by status
    if status and status != '':
        investments = UserInvestment.objects.annotate(search=SearchVector('status'),).filter(search__icontains=status)

    return investments
