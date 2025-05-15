from django.urls import path
from .views import (
    index, about, faqs, plans, partnerships, contact,
    privacy_policy
)


urlpatterns = [
    path('', index, name='index'),
    path('about/', about, name='about'),
    path('faqs/', faqs, name='faqs'),
    path('plans/', plans, name='plans'),
    path('partnerships/', partnerships, name='partnerships'),
    path('contact/', contact, name='contact'),
    path("privacy-policy/", privacy_policy, name="privacy-policy"),
]