from django.urls import path, include
from rest_framework import routers
from . import views


urlpatterns = [
    # path('submit_contact/', views.submit_contact, name='submit_contact'),
    path('contact/', views.contact_view, name='contact_view'),
    path('contact/success/', views.contact_success, name='contact_success'), 
]
