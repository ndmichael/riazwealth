from django.shortcuts import render

# Create your views here.


def index(request):
    context = {
        'title': 'Wealth Wheel Capital Investment'
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

def offers(request):
    context = {
        'title': 'Investment Offers'
    }
    return render(request, 'pages/offers.html', context)

def partnerships(request):
    context = {
        'title': 'Partnerships and Loan'
    }
    return render(request, 'pages/partnerships.html', context)

def contact(request):
    context = {
        'title': 'Contact Us'
    }
    return render(request, 'pages/contact.html', context)