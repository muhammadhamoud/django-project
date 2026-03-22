import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import smart_bytes
from django.utils.http import urlsafe_base64_encode
from jwt import DecodeError, ExpiredSignatureError
from rest_framework import status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import Notification, NotificationRecipient

User = get_user_model()


def send_verification_email(
    user_id, receiver, current_site, mail_subject, email_template
):
    user = User.objects.get(id=user_id)
    token = RefreshToken.for_user(user).access_token

    message = render_to_string(
        email_template,
        {
            "domain": current_site,
            "token": token,
        },
    )
    email = EmailMessage(
        mail_subject, message, "mydjangoproject87@gmail.com", to=[receiver]
    )
    email.content_subtype = "html"
    # SendEmailThread(email).start()
    email.send()


def send_reset_password_email(
    user_id, receiver, current_site, mail_subject, email_template
):
    user = User.objects.get(id=user_id)
    uidb64 = urlsafe_base64_encode(smart_bytes(user.pk))
    token = PasswordResetTokenGenerator().make_token(user)
    message = render_to_string(
        email_template,
        {
            "domain": current_site,
            "user": user,
            "token": token,
            "uid": uidb64,
        },
    )
    email = EmailMessage(
        mail_subject, message, "mydjangoproject87@gmail.com", to=[receiver]
    )
    email.content_subtype = "html"
    # SendEmailThread(email).start()
    email.send()


def activate_user(token):
    try:
        token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        # decode the incoming token
        user_id = token.get("user_id")

        user = User.objects.get(id=user_id)

        if not user.is_verified:
            user.is_verified = True
            user.save()

            return Response(
                {
                    "detail": "Thank you for your email confirmation. Now you can login your account."
                },
                status=status.HTTP_200_OK,
            )

        return Response(
            {"detail": "Your account is already verified."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except ExpiredSignatureError:
        # if token expired
        return Response(
            {"detail": "Activation link is expired"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except DecodeError:
        # if token is not valid
        return Response(
            {"detail": "Token is invalid"},
            status=status.HTTP_400_BAD_REQUEST,
        )



from django.core.mail import EmailMessage
from django.conf import settings


class Util:
    @staticmethod
    def send_email(data):
        email = EmailMessage(to=[data['to_email']], subject=data['email_subject'], body=data['email_body'])
        # Optional: add a plain text version of the email
        email.content_subtype = 'html'
        email.send(fail_silently=True)


class EmailTemplates:
    def email_verfication_template(full_name, url):
        email_style = """
    <style>
      /* CSS styling */
      body {
        font-family: Arial, Helvetica, sans-serif;
        font-size: 16px;
        line-height: 1.5;
        color: #333333;
        background-color: #a2a1a1;
        padding: 20px;
      }
      h1,
      h2,
      h3,
      h4,
      h5,
      h6 {
        margin-top: 0;
      }
      a {
        color: #0e273a;
      }
      .button {
        display: inline-block;
        font-weight: 400;
        color: #ffffff;
        text-color: white;
        text-align: center;
        vertical-align: middle;
        background-color: #0e273a;
        border: 1px solid #0e273a;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        text-decoration: none;
      }
      .button:hover {
        background-color: #3e607e;
        border-color: #3e607e;
      }
    </style>
        """
        email_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8" />
            <title>email</title>
            {email_style}
        </head>
        <body>
            <h1>Email Verification Confirmation</h1>
            <p>Dear {full_name},</p>
            <p>
            Thank you for signing up for our {settings.WEBISTE_NAME} service. To complete your registration,
            please click on the link below to verify your email address:
            </p>
            <p style="text-align: left"><a href="{url}" class="button">Verify Email Address</a></p>
           
            <p>If you did not sign up for our service, please disregard this email.</p>
            <p>Best regards,</p>
            <p>The {settings.WEBISTE_NAME} Team</p>
            <hr />
        </body>
    </html>
        """

        return email_body



from rest_framework import renderers
import json


class Renderer(renderers.JSONRenderer):
    charset = 'utf-8'

    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = ''
        if 'ErrorDetail' in str(data):
            response = json.dumps({'errors': data})
        else:
            response = json.dumps({'data': data})
        return response


from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.conf import settings
from django.db import models

from rest_framework import permissions as rest_permissions

class IsAdminUser(rest_permissions.BasePermission):
    """
    Allows access only to admin users.
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_admin)
    


from rest_framework import permissions


class IsUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role.id == 1


class IsBoardMember(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role.id == 2


class IsEditor(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role.id == 3


class IsMember(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user.role.id == 4


class IsExpensePermission(permissions.BasePermission):

    def has_permission(self, request, view):
        method = ['PATCH', 'POST', 'PUT', 'DELETE']
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in method:
            return request.user.role.id < 4


class IsDonationPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        method = ['PATCH', 'POST', 'PUT', 'DELETE']
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in method:
            return request.user.role.id < 4


class IsCampaignPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        method = ['PATCH', 'POST', 'PUT', 'DELETE']
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in method:
            return request.user.role.id < 4


class IsUsersPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        method = ['PATCH', 'POST', 'PUT']
        if request.method in permissions.SAFE_METHODS:
            return True
        elif request.method in method:
            return request.user.role.id <= 4
        


from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


def send_notification(title, message, users=None, created_by=None, level="info", link=None, alert=False,send_to_all=False):
    notification = Notification.objects.create(
        title=title,
        message=message,
        level=level,
        link=link,
        alert=alert,
        created_by=created_by,
        send_to_all=send_to_all,
    )

    if send_to_all:
        users = User.objects.filter(is_active=True)

    if users is None:
        return notification

    recipient_rows = [
        NotificationRecipient(notification=notification, user=user)
        for user in users
    ]
    NotificationRecipient.objects.bulk_create(recipient_rows, ignore_conflicts=True)
    return notification