from django.urls import path
from .views import (
    index, about, faqs, offers, partnerships, contact
)


urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('faqs/', faqs, name='faqs'),
    path('offers/', offers, name='offers'),
    path('partnerships/', partnerships, name='partnerships'),
    path('contact/', contact, name='contact'),
]