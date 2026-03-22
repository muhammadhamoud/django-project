from django.urls import path
from .views import register_view, login_view, logout_view, resend_verification_view, reset_password_view, forgot_password_view, user_create_view, verify_email_view

app_name = "accounts"

urlpatterns = [
    path("accounts/register/", register_view, name="register"),
    path("accounts/login/", login_view, name="login"),
    path("accounts/logout/", logout_view, name="logout"),
    path("accounts/forgot-password/", forgot_password_view, name="forgot_password"),
    path("accounts/reset-password/<uidb64>/<token>/", reset_password_view, name="reset_password"),
    path("accounts/resend-verification/", resend_verification_view, name="resend_verification"),
    path("accounts/verify-email/", verify_email_view, name="verify_email"),

    path("accounts/users/create/", user_create_view, name="user_create"),
]
 
from .views import (
    notification_center_view, 
    notification_send_view,
    notification_mark_read_view,
    notification_mark_all_read_view,
)
urlpatterns += [ 
    path("accounts/notifications/", notification_center_view, name="notification_center"),
    path("accounts/notifications/send/", notification_send_view, name="notification_send"),
    path("accounts/notifications/<int:pk>/read/", notification_mark_read_view, name="notification_mark_read"),
    path("accounts/notifications/read-all/", notification_mark_all_read_view, name="notification_mark_all_read"),
]

from .views import (
    user_list_view,
    user_detail_view,
    current_user_view,
    profile_view,
)

urlpatterns += [
    path("accounts/users/", user_list_view, name="user_list"),
    path("accounts/users/<str:id>/", user_detail_view, name="user_detail"),
    # path("users/<int:user_id>/delete/", user_delete_view, name="user_delete"),
    path("accounts/me/", current_user_view, name="current_user"),
    path("accounts/profile/", profile_view, name="profile"),
]