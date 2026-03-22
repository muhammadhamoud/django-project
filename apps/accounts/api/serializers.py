
from rest_framework import serializers
from accounts.models import CustomUser, UserProfile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = CustomUser
        fields = ["id", "email", "first_name", "last_name", "password"]

    def create(self, validated_data):
        return CustomUser.objects.create_user(**validated_data)
    

from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    tokens = serializers.DictField(read_only=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed("Invalid credentials")

        if not user.is_active:
            raise AuthenticationFailed("Account disabled")

        return {
            "id": str(user.id),
            "email": user.email,
            "tokens": user.tokens(),
        }
    
from accounts.models import Role, Permission


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ["id", "code", "name"]


class RoleSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Role
        fields = ["id", "code", "name", "permissions"]


class UserProfileSerializer(serializers.ModelSerializer):

    roles = RoleSerializer(many=True, read_only=True)
    direct_permissions = PermissionSerializer(many=True, read_only=True)

    company = serializers.StringRelatedField()
    department = serializers.StringRelatedField()
    job_title = serializers.StringRelatedField()
    properties = serializers.StringRelatedField(many=True)

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "roles",
            "direct_permissions",
            "company",
            "department",
            "job_title",
            "properties",
            "disabled",
        ]


class UserSerializer(serializers.ModelSerializer):

    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "is_staff",
            "profile",
        ]


class MeSerializer(serializers.ModelSerializer):

    roles = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "is_active",
            "roles",
        ]

    def get_roles(self, obj):
        if hasattr(obj, "profile"):
            return list(obj.profile.roles.values_list("name", flat=True))
        return []
    

class UpdateUserProfileSerializer(serializers.ModelSerializer):

    roles = serializers.PrimaryKeyRelatedField(
        queryset=Role.objects.all(),
        many=True,
        required=False
    )

    properties = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.properties.rel.model.objects.all(),
        many=True,
        required=False
    )

    class Meta:
        model = UserProfile
        fields = [
            "roles",
            "company",
            "department",
            "job_title",
            "properties",
            "disabled",
        ]

    def update(self, instance, validated_data):

        roles = validated_data.pop("roles", None)
        properties = validated_data.pop("properties", None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        if roles is not None:
            instance.roles.set(roles)

        if properties is not None:
            instance.properties.set(properties)

        instance.save()
        return instance



class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = CustomUser
        fields = ['token']


























# from rest_framework import serializers
# from accounts.models import CustomUser as User, UserProfile #TODO change this
# from django.contrib import auth
# from rest_framework.exceptions import AuthenticationFailed, NotAcceptable
# from django.contrib.auth.tokens import PasswordResetTokenGenerator
# from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
# from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
# from django.contrib.sites.shortcuts import get_current_site
# from django.urls import reverse
# # from addresses.api.serializers import (
# #     CountrySerializer,
# #     CitySerializer,
# #     AddressTypeSerializer,
# #     AddressFormatSerializer,
# #     StateSerializer,
# # )
# # from addresses.models import Address
# # from home.blogs.api.serializers import FavoritePostSerializer
# from utils import Util


# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(max_length=60, min_length=8, write_only=True)

#     class Meta:
#         model = User
#         fields = '__all__' #['email', 'full_name', 'password', 'id']

#     def validate(self, attrs):
#         return attrs

#     def create(self, validated_data):
#         return User.objects.create_user(**validated_data)


# class EmailVerificationSerializer(serializers.ModelSerializer):
#     token = serializers.CharField(max_length=555)

#     class Meta:
#         model = User
#         fields = ['token']


# class LoginSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(max_length=255, min_length=3)
#     password = serializers.CharField(max_length=58, min_length=6, write_only=True)
#     tokens = serializers.DictField(read_only=True)

#     class Meta:
#         model = User
#         fields = ['id', 'email', 'password', 'tokens']

#     def validate(self, attrs):
#         email = attrs.get('email', '')
#         password = attrs.get('password', '')

#         user = auth.authenticate(email=email, password=password)
#         if not user:
#             raise NotAcceptable("Email or Password Incorrect, try again")
#         if not user.is_active:
#             raise NotAcceptable("Account Disabled, contact admin")
#         if not user.is_verified:
#             raise NotAcceptable("Email is not verified.")
#         return {
#             'id': user.id,
#             'email': user.email,
#             'tokens': user.tokens()
#         }


# class ResetPasswordWithEmailSerializer(serializers.Serializer):
#     email = serializers.EmailField(min_length=2)

#     class Meta:
#         fields = ['email']


# class PasswordTokenCheckSerializer(serializers.Serializer):
#     token = serializers.CharField(min_length=1, write_only=True)
#     uidb64 = serializers.CharField(min_length=1, write_only=True)

#     class Meta:
#         fields = ['token', 'token']

class ValidateTokenCheckSerializer(serializers.Serializer):
    token = serializers.CharField(min_length=1, write_only=True)

    class Meta:
        fields = ['token', 'token']



# class SetNewPasswordSerializer(serializers.Serializer):
#     password = serializers.CharField(min_length=8, write_only=True)
#     token = serializers.CharField(min_length=1, write_only=True)
#     uidb64 = serializers.CharField(min_length=1, write_only=True)

#     class Meta:
#         fields = ['password', 'token', 'uidb64']

#     def validate(self, attrs):
#         try:
#             password = attrs.get('password')
#             token = attrs.get('token')
#             uidb64 = attrs.get('uidb64')

#             id = force_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(id=id)

#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 raise AuthenticationFailed('The reset link is invalid', 401)

#             user.set_password(password)
#             user.save()
#         except Exception as err:
#             raise AuthenticationFailed('The reset link is invalid', 401)
#         return super().validate(attrs)


# class UsersSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'


# class MeAPIViewSerializer(serializers.ModelSerializer):
#     role = serializers.StringRelatedField()

#     class Meta:
#         model = User
#         fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'status', 'role']


# # class AddressSerializer(serializers.ModelSerializer):
# #     country = CountrySerializer()
# #     # city = CitySerializer()
# #     type = AddressTypeSerializer()
# #     format = AddressFormatSerializer()
# #     state = StateSerializer()
# #     class Meta:
# #         model = Address
# #         fields = '__all__'


# class ProfileSerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(source="user.email", read_only=True)
#     first_name = serializers.CharField(source="user.first_name")
#     last_name = serializers.CharField(source="user.last_name")
#     status = serializers.CharField(source="user.status")
#     # favoritepost = FavoritePostSerializer(many=True, read_only=True)
#     # address = AddressSerializer(many=True, read_only=True)
#     address = serializers.SerializerMethodField()

#     class Meta:
#         model = UserProfile
#         # fields = '__all__'
#         fields = [
#             "id",
#             "email",
#             "first_name",
#             "last_name",
#             "status",
#             "image",
#             "bio",
#             "birth_date",
#             "created_date",
#             "modified_date",
#             'address'
#         ]

#     # def to_representation(self, instance):
#     #     representation = super().to_representation(instance)
#     #     address_data = AddressSerializer(instance.user.address_set.all(), many=True).data
#     #     representation['address'] = address_data
#     #     return representation

#     # def get_address(self, instance):
#     #     address_queryset = instance.user.address.all()
#     #     address_serializer = AddressSerializer(address_queryset, many=True)
#     #     return address_serializer.data
    
#     def get_serializer_context(self):
#         context = super().get_serializer_context()
#         context['request'] = self.request
#         return context
    

# from rest_framework import serializers
# from accounts.models import CustomUser


# class UserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = CustomUser
#         fields = "__all__"