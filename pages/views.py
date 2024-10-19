from django.shortcuts import render
from .forms import ContactForm
from investments.models import InvestmentPlan

# Create your views here.


def index(request):
    context = {
        'title': 'RiazVest Capital Investment'
    }
    return render(request, "pages/index.html", context)

def about(request):
    context = {
        'title': 'About Us'
    }
    return render(request, 'pages/about.html', context)

def faqs(request):
    context = {
        'title': 'FAQs'
    }
    return render(request, 'pages/faqs.html', context)

def plans(request):
    plans = InvestmentPlan.objects.all().order_by('-min_amount')
    context = {
        'title': 'Investment Offers',
        'plans': plans,
    }
    return render(request, 'pages/plans.html', context)

def partnerships(request):
    context = {
        'title': 'Partnerships and Loan'
    }
    return render(request, 'pages/partnerships.html', context)

def contact(request):
    form = ContactForm
    context = {
        'title': 'Contact Us',
        'form': form,
    }
    return render(request, 'pages/contact.html', context)