from django.urls import path, include
from rest_framework import routers
from . import views

# router = routers.DefaultRouter()
# router.register(r'subscribers', SubscriberViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    # path('api/subscribe/', subscribe, name='subscribe'),
    # path('api/unsubscribe/<email>/', SubscriberViewSet.as_view({'get': 'unsubscribe'}), name='unsubscribe'),
    # path('api/resubscribe/<email>/', SubscriberViewSet.as_view({'get': 'resubscribe'}), name='resubscribe'),
    
    # path('subscribe/', views.SubscriberViewSet.as_view({'post': 'manage_subscription', 'name': 'subscribe'})),
    # path('unsubscribe/', views.SubscriberViewSet.as_view({'post': 'manage_subscription', 'name': 'unsubscribe'})),
    # path('resubscribe/', views.SubscriberViewSet.as_view({'post': 'manage_subscription', 'name': 'resubscribe'})),

    # TODO recently commented
    # path('subscribe/', views.SubscriberViewSet.as_view({'post': 'subscribe'})),
    # path('unsubscribe/<email>/', views.SubscriberViewSet.as_view({'post': 'unsubscribe'})),
    # path('resubscribe/<email>/', views.SubscriberViewSet.as_view({'post': 'resubscribe'})),

    # path('contactus/', views.submit_contact, name='contactus'),

]
