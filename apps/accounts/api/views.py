
from rest_framework import generics, status, permissions, views
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.urls import reverse
from django.conf import settings

import jwt

from accounts.models import CustomUser, UserProfile
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UserSerializer,
    UserProfileSerializer,
    UpdateUserProfileSerializer,
    MeSerializer,
    ValidateTokenCheckSerializer
)

from utils import Util, EmailTemplates, Renderer

User = get_user_model()


# =====================================================
# AUTH
# =====================================================

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (Renderer,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        # Email verification
        token = RefreshToken.for_user(user).access_token
        relative_link = reverse("accounts:verify_email")
        abs_url = f"http://{request.get_host()}{relative_link}?token={token}"

        email_body = EmailTemplates.email_verfication_template(user.email, abs_url)
        Util.send_email({
            "to_email": user.email,
            "email_body": email_body,
            "email_subject": "Verify your email"
        })

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmail(APIView):
    renderer_classes = (Renderer,)

    def get(self, request):
        token = request.GET.get("token")

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            user = CustomUser.objects.get(id=payload["user_id"])

            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({"message": "Email verified"}, status=200)

        except jwt.ExpiredSignatureError:
            return Response({"error": "Token expired"}, status=400)
        except jwt.DecodeError:
            return Response({"error": "Invalid token"}, status=400)


class LoginApiView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    renderer_classes = (Renderer,)
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=200)


# =====================================================
# PASSWORD RESET
# =====================================================

class ResetPasswordWithEmail(APIView):
    def post(self, request):
        email = request.data.get("email")

        if not CustomUser.objects.filter(email=email).exists():
            return Response({"error": "Email not found"}, status=404)

        user = CustomUser.objects.get(email=email)

        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        link = reverse("accounts:password_reset_confirm", kwargs={
            "uidb64": uidb64,
            "token": token
        })

        abs_url = f"http://{request.get_host()}{link}"

        Util.send_email({
            "to_email": user.email,
            "email_body": f"Reset password: {abs_url}",
            "email_subject": "Reset Password"
        })

        return Response({"message": "Reset link sent"}, status=200)


class PasswordTokenCheckAPI(APIView):
    def get(self, request, uidb64, token):
        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"error": "Invalid token"}, status=400)

            return Response({"success": True}, status=200)

        except Exception:
            return Response({"error": "Invalid token"}, status=400)


class SetNewPasswordAPIView(APIView):
    def post(self, request):
        password = request.data.get("password")
        token = request.data.get("token")
        uidb64 = request.data.get("uidb64")

        try:
            user_id = smart_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"error": "Invalid token"}, status=400)

            user.set_password(password)
            user.save()

            return Response({"message": "Password reset successful"}, status=200)

        except Exception:
            return Response({"error": "Invalid request"}, status=400)


# =====================================================
# USERS
# =====================================================

# class UserListAPIView(generics.ListCreateAPIView):
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         return CustomUser.objects.all().select_related("profile")

#     def perform_create(self, serializer):
#         serializer.save()

from accounts.permissions import permission_required, property_permission_required
from properties.models import Property

from rest_framework.exceptions import PermissionDenied

class UserListAPIView(generics.ListCreateAPIView):
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [permission_required("user.create")()]
        return [permission_required("user.view")()]

    def get_queryset(self):

        user = self.request.user
        profile = user.profile

        # # ✅ Admin can see all
        # if user.is_superuser or user.is_admin:
        #     return CustomUser.objects.all()

        # ✅ Must be supervisor
        if not (
            profile.roles.filter(code="supervisor").exists()
            or profile.roles.filter(code="super_admin").exists()
        ):
            raise PermissionDenied("Only supervisors can view users")

        # ✅ Only users within assigned properties
        return CustomUser.objects.filter(
            profile__properties__in=profile.properties.all()
        ).distinct()


class UserDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    lookup_field = "id"

    def get_permissions(self):

        if self.request.method == "GET":
            return [property_permission_required("user.view")()]

        elif self.request.method in ["PUT", "PATCH"]:
            return [property_permission_required("user.edit")()]

        elif self.request.method == "DELETE":
            return [property_permission_required("user.delete")()]

        return super().get_permissions()

    def get_queryset(self):

        profile = self.request.user.profile

        return CustomUser.objects.filter(
            profile__properties__in=profile.properties.all()
        ).distinct()


class CurrentUsersAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = MeSerializer(request.user)
        return Response(serializer.data)


# =====================================================
# PROFILE
# =====================================================

class ProfileAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user.profile

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return UpdateUserProfileSerializer
        return UserProfileSerializer

# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.response import Response
# from rest_framework import status, generics, views
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from accounts.models import CustomUser, UserProfile
# from accounts.api.paginations import ProfileFavoritePostPagination
# from accounts.services import update_profile
# # from home.blogs.api.serializers import FavoritePostSerializer
# from .serializers import ProfileSerializer, RegisterSerializer, EmailVerificationSerializer, LoginSerializer, \
#     ResetPasswordWithEmailSerializer, SetNewPasswordSerializer, PasswordTokenCheckSerializer, MeAPIViewSerializer, \
#     UsersSerializer, ValidateTokenCheckSerializer
# from django.contrib.sites.shortcuts import get_current_site
# from django.urls import reverse
# import jwt
# from django.conf import settings
# from drf_yasg.utils import swagger_auto_schema
# from drf_yasg import openapi
# from rest_framework import permissions

# from utils import Renderer
# from utils import IsAdminUser
# from utils import EmailTemplates, Util

# # from services import customPermission
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.generics import get_object_or_404
# from django.core.cache import cache


# User = settings.AUTH_USER_MODEL
# from django.contrib.auth import get_user_model

def verify_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload.get('user_id')
        
        # Use get_user_model() to handle custom user models
        User = get_user_model()
        user = CustomUser.objects.get(id=user_id)
        
        return user
    except jwt.ExpiredSignatureError:
        # Handle expired token
        raise jwt.ExpiredSignatureError('Token has expired')
    except jwt.InvalidTokenError:
        # Handle invalid token
        raise jwt.InvalidTokenError('Token is invalid')
    except User.DoesNotExist:
        # Handle user not found
        raise User.DoesNotExist('User not found')


# class RegisterView(generics.GenericAPIView):
#     serializer_class = RegisterSerializer
#     renderer_classes = (Renderer,)
    
#     def post(self, request):
#         user_data = request.data
#         email = user_data.get('email')

#         # Check if the user with the given email already exists
#         if CustomUser.objects.filter(email=email).exists():
#             return Response({'error': 'User with this email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

#         serializer = self.serializer_class(data=user_data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()

#         user_data = serializer.data

#         user = CustomUser.objects.get(email=user_data['email'])
#         token = RefreshToken.for_user(user).access_token

#         relative_link = reverse('verify-email')
#         current_site = get_current_site(request).domain
#         abs_url = 'http://'+current_site+relative_link+"?token="+str(token)

#         email_body_html = EmailTemplates.email_verfication_template(user.email, abs_url)

#         data = {'to_email': user.email, 'email_body': email_body_html, 'email_subject': 'Verify your email'}
#         Util.send_email(data)

#         return Response(user_data, status=status.HTTP_201_CREATED)
    
    
#     # def post(self, request):
#     #     user = request.data
#     #     serializer = self.serializer_class(data=user)
#     #     serializer.is_valid(raise_exception=True)
#     #     serializer.save()

#     #     user_data = serializer.data

#     #     user = CustomUser.objects.get(email=user_data['email'])
#     #     token = RefreshToken.for_user(user).access_token

#     #     relative_link = reverse('verify-email')
#     #     current_site = get_current_site(request).domain
#     #     abs_url = 'http://'+current_site+relative_link+"?token="+str(token)

#     #     # email_body = 'Hi {} Use below link to verify your email \n {}'.format(user.full_name, abs_url)
#     #     email_body_html = EmailTemplates.email_verfication_template(user.email, abs_url)

#     #     data = {'to_email': user.email, 'email_body': email_body_html, 'email_subject': 'Verify your email'}
#     #     Util.send_email(data)
    
#     #     return Response(user_data, status=status.HTTP_201_CREATED)


# class VerifyEmail(APIView):
#     serializer_class = EmailVerificationSerializer
#     renderer_classes = (Renderer,)

#     token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

#     # @swagger_auto_schema(manual_parameters=[token_param_config])
#     def get(self, request):
#         token = request.GET.get('token')
       
#         try:
#             payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
#             user = CustomUser.objects.get(id=payload['user_id'])
#             if not user.is_verified:
#                 user.is_verified = True
#                 user.save()
#             return Response({'email': 'Successfully Verified'}, status=status.HTTP_201_CREATED)
        
#         except jwt.exceptions.DecodeError as err:
#             return Response({'email': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)


class TokenValidationView(generics.GenericAPIView):
    serializer_class = ValidateTokenCheckSerializer

    def post(self, request, *args, **kwargs):
        token = request.GET.get('token')  # Retrieve the token from URL parameters

        if not token:
            return Response({'error': 'Token is missing'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = verify_token(token)

            return Response({'message': 'Token is valid', 'user_id': user.id}, status=status.HTTP_200_OK)

        except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
            return Response({'error': 'Invalid or expired token'}, status=status.HTTP_400_BAD_REQUEST)


# class LoginApiView(generics.GenericAPIView):
#     serializer_class = LoginSerializer
#     renderer_classes = (Renderer,)
#     # Remove authentication_classes and permission_classes
#     authentication_classes = []
#     permission_classes = []

#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return serializer.is_valid()


# class ResetPasswordWithEmail(generics.GenericAPIView):
#     serializer_class = ResetPasswordWithEmailSerializer
#     renderer_classes = (Renderer,)

#     def post(self, request):
#         data = {'request': request, 'data': request.data}
#         serializer = self.serializer_class(data=data)
#         email = request.data['email']

#         if CustomUser.objects.filter(email=email).exists():
#             user = CustomUser.objects.get(email=email)

#             uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
#             token = PasswordResetTokenGenerator().make_token(user)
#             # current_site = get_current_site(request=request).domain
#             current_site = f"https://{settings.DOMAIN}"

#             relative_link = reverse('password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
#             # print(relative_link)
#             abs_url = 'http://' + current_site + relative_link

#             email_body = 'Hi, \n Use below link to reset your password \n {}'.format(abs_url)
#             data = {'to_email': user.email, 'email_body': email_body, 'email_subject': 'Reset your password'}
            
#             Util.send_email(data)

#             return Response({'success': 'We have send you a link to reset your password'}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'not found email'}, status=status.HTTP_406_NOT_ACCEPTABLE)


# class PasswordTokenCheckAPI(generics.GenericAPIView):
#     serializer_class = PasswordTokenCheckSerializer
#     renderer_classes = (Renderer,)
#     authentication_classes = []
#     permission_classes = []
#     def get(self, request, uidb64, token):
#         try:
#             id = smart_str(urlsafe_base64_decode(uidb64))
#             user = CustomUser.objects.get(id=id)

#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 return Response({'error': 'Token is not valid, please request a new one'}, status.HTTP_401_UNAUTHORIZED)

#             return Response({'success': True, 'message': 'Credential valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
        
#         except DjangoUnicodeDecodeError as err:
#             return Response({'error': 'Token is not valid, please request a new one'}, status.HTTP_401_UNAUTHORIZED)


# class SetNewPasswordAPIView(generics.GenericAPIView):
#     serializer_class = SetNewPasswordSerializer
#     renderer_classes = (Renderer,)
#     authentication_classes = []
#     permission_classes = []
    
#     def patch(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response({'success': True, 'message': 'Password reset success'}, status=status.HTTP_200_OK)


# class UserListAPIView(generics.ListCreateAPIView):
#     serializer_class = UsersSerializer
#     queryset = CustomUser.objects.all()
#     renderer_classes = (Renderer,)
#     permission_classes = (IsAdminUser,)

#     def perform_create(self, serializer):
#         return serializer.save()

#     def get_queryset(self):
#         return self.queryset


# class UserDetailsAPIView(generics.RetrieveUpdateDestroyAPIView):
#     serializer_class = UsersSerializer
#     queryset = CustomUser.objects.all()
#     renderer_classes = (Renderer,)
#     permission_classes = (permissions.IsAuthenticated)
#     lookup_field = 'id'

#     def get_queryset(self):
#         return self.queryset


# class CurrentUsersAPIView(views.APIView):
#     serializer_class = MeAPIViewSerializer
#     renderer_classes = (Renderer,)
#     permission_classes = (permissions.IsAuthenticated, )

#     def get(self, request):
#         user_info = CustomUser.objects.get(id=request.user.id)
#         serializer = self.serializer_class(user_info)

#         return Response(serializer.data, status=status.HTTP_200_OK)


# # class ProfileAPIView(generics.RetrieveUpdateAPIView):
# #     serializer_class = ProfileSerializer
# #     queryset = (
# #         Profile.objects.select_related("user")
# #         .prefetch_related("favoritepost__post__category", "favoritepost__post__author")
# #         .all()
# #     )
# #     permission_classes = [IsAuthenticated]

# #     def get_object(self):
# #         queryset = self.get_queryset()
# #         obj = get_object_or_404(queryset, user=self.request.user)
# #         return obj

# #     def retrieve(self, request, *args, **kwargs):
# #         profile = self.get_object()
# #         favorite_post = cache.get(f"profile_{profile.id}_favorite_post")
# #         if not favorite_post:
# #             favorite_post = profile.favoritepost.all()
# #             cache.set(f"profile_{profile.id}_favorite_post", favorite_post, timeout=300)
# #         paginator = ProfileFavoritePostPagination()
# #         page_obj = paginator.paginate_queryset(favorite_post, request=self.request)
# #         serializer = ProfileSerializer(profile, context={"request": request})
# #         data = serializer.data

# #         data["favoritepost"] = FavoritePostSerializer(
# #             page_obj, many=True, context={"request": request}
# #         ).data
# #         return paginator.get_paginated_response(data)

# #     def update(self, request, *args, **kwargs):
# #         instance = self.get_object()

# #         serializer = self.get_serializer(
# #             instance=instance,
# #             data=request.data,
# #             partial=True,
# #         )
# #         serializer.is_valid(raise_exception=True)
# #         validated_data = serializer.validated_data

# #         try:
# #             profile = update_profile(
# #                 instance=instance,
# #                 validated_data=validated_data,
# #             )
# #         except Exception as e:
# #             return Response(
# #                 {"detail": str(e)},
# #                 status=status.HTTP_400_BAD_REQUEST,
# #             )

# #         serializer = ProfileSerializer(profile, context={"request": request})
# #         return Response(serializer.data, status=status.HTTP_200_OK)


# class ProfileAPIView(generics.RetrieveUpdateAPIView):
#     """
#     View for retrieving and updating a user's profile.
#     """
#     serializer_class = ProfileSerializer
#     queryset = UserProfile.objects.select_related("user").prefetch_related("user__address").all()
#     permission_classes = [IsAuthenticated]

#     def get_object(self):
#         queryset = self.get_queryset()
#         obj = get_object_or_404(queryset, user=self.request.user)
#         return obj

#     def update(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(
#             instance=instance,
#             data=request.data,
#             partial=True,
#         )
#         serializer.is_valid(raise_exception=True)
#         validated_data = serializer.validated_data

#         try:
#             profile = update_profile(
#                 instance=instance,
#                 validated_data=validated_data,
#             )
#         except Exception as e:
#             return Response(
#                 {"detail": str(e)},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         serializer = ProfileSerializer(profile, context={"request": request})
#         return Response(serializer.data, status=status.HTTP_200_OK)
    

# from rest_framework.viewsets import ModelViewSet
# from rest_framework.permissions import IsAuthenticated

# from accounts.models import CustomUser
# from api.serializers import UserSerializer
# from accounts.querysets import user_visibility_queryset


# class UserViewSet(ModelViewSet):

#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):

#         return user_visibility_queryset(self.request)