from django.urls import path, include
from rest_framework import routers
from . import views


app_name = "communication"
urlpatterns = [
    # path('submit_contact/', views.submit_contact, name='submit_contact'),
    path('contact/', views.contact_view, name='contact_us'),
    path("subscribe/", views.subscriber_view, name="subscribe"),
    # path('contact/success/', views.contact_success, name='contact_success'), 
]
