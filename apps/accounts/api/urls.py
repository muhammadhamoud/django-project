from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

app_name = "accountsapi"

urlpatterns = [
    # -----------------------------
    # Auth
    # -----------------------------
    path("auth/register/", views.RegisterView.as_view(), name="register"),
    path("auth/login/", views.LoginApiView.as_view(), name="login"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # Email verification (optional)
    path("auth/verify-email/", views.VerifyEmail.as_view(), name="verify_email"),

    # -----------------------------
    # Password Reset
    # -----------------------------
    path("auth/password/reset/", views.ResetPasswordWithEmail.as_view(), name="request_reset_password"),
    path("auth/password/reset/<uidb64>/<token>/", views.PasswordTokenCheckAPI.as_view(), name="password_reset_confirm"),
    path("auth/password/reset/complete/", views.SetNewPasswordAPIView.as_view(), name="password_reset_complete"),
    path("auth/token/validate/", views.TokenValidationView.as_view(), name="token_validation"),

    # -----------------------------
    # Users
    # -----------------------------
    path("users/", views.UserListAPIView.as_view(), name="user_list"),
    path("users/<uuid:id>/", views.UserDetailsAPIView.as_view(), name="user_detail"),

    # -----------------------------
    # Current User
    # -----------------------------
    path("users/me/", views.CurrentUsersAPIView.as_view(), name="current_user"),

    # -----------------------------
    # Profile
    # -----------------------------
    path("profile/", views.ProfileAPIView.as_view(), name="profile"),
]

# from django.urls import path
# from . import views
# from rest_framework_simplejwt.views import (
#     TokenRefreshView,
# )
# app_label ='accounts'

# urlpatterns = [
#     path('register', views.RegisterView.as_view(), name='register'),
#     path('verify-email', views.VerifyEmail.as_view(), name='verify-email'),
#     path('login', views.LoginApiView.as_view(), name='login'),
#     path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    
#     path('request-reset-password', views.ResetPasswordWithEmail.as_view(), name='request-reset-password'),
#     path('password-reset/<uidb64>/<token>', views.PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
#     path('password-reset-complete', views.SetNewPasswordAPIView.as_view(), name='password-reset-complete'),
#     path('token-validation/', views.TokenValidationView.as_view(), name='token_validation'),

    
#     path('get_user/', views.CurrentUsersAPIView.as_view(), name='get_user'),
#     path('users', views.UserListAPIView.as_view(), name='all-users'),
#     path('<int:id>', views.UserDetailsAPIView.as_view(), name="single-user"),

#     path("profile/", views.ProfileAPIView.as_view(), name="profile"),
# ]


# from rest_framework.routers import DefaultRouter
# from .views import UserViewSet

# router = DefaultRouter()

# router.register("users", UserViewSet)

# urlpatterns = router.urls