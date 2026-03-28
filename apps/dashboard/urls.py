from django.urls import path
from . import views

app_name = "dashboard"

urlpatterns = [
    path('dashboard/', views.home, name='home'),
    path('analytics/', views.analytics, name='analytics'),
    path('metrics/', views.metrics, name='metrics'),
    # path('reports/', views.reports, name='reports'),
    # path('users/', views.users, name='users'),

]