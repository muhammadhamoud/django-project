import uuid
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from core.handle_images import compress_image
from core.models import base_image_path, validate_image_extension
from django.utils.text import slugify

# =====================================================
# BASE MODELS (Soft Delete + Audit)
# =====================================================

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


class AuditLog(models.Model):
    ACTIONS = (
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
        ("ASSIGN", "Assign"),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=20, choices=ACTIONS)
    target_model = models.CharField(max_length=100)
    target_id = models.CharField(max_length=100)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


# =====================================================
# PERMISSION SYSTEM
# =====================================================

class PermissionGroup(BaseModel):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Permission Group"
        verbose_name_plural = "Permission Groups"


class Permission(BaseModel):
    code = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=150)

    group = models.ForeignKey(
        PermissionGroup,
        on_delete=models.CASCADE,
        related_name="permissions"
    )

    def __str__(self):
        return f"{self.group.name} - {self.name}"


class Company(BaseModel):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"


class Role(BaseModel):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.CASCADE)

    permissions = models.ManyToManyField(Permission, blank=True, related_name="roles")

    is_admin_role = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class RoleTemplate(BaseModel):
    name = models.CharField(max_length=100, unique=True)
    permissions = models.ManyToManyField(Permission, blank=True)

    def create_role(self, company=None):
        role = Role.objects.create(name=self.name, code=self.name.lower().replace(" ", "_"), company=company)
        role.permissions.set(self.permissions.all())
        return role

    class Meta:
        verbose_name = "Role Template"
        verbose_name_plural = "Role Templates"


# =====================================================
# ORG STRUCTURE
# =====================================================

class Department(BaseModel):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Department"
        verbose_name_plural = "Departments"

class JobTitle(BaseModel):
    name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Job Title"
        verbose_name_plural = "Job Titles"

# =====================================================
# USER
# =====================================================

class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_admin", True)

        return self.create_user(email, password, **extra_fields)
    

class CustomUser(AbstractBaseUser, PermissionsMixin, BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"

    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"


    def save(self, *args, **kwargs):
        if not self._state.adding:
            old = CustomUser.objects.filter(pk=self.pk).only("email").first()
            if old and old.email != self.email:
                raise ValueError("Email cannot be changed")
        self.first_name = str(self.first_name).title()
        self.last_name = str(self.last_name).title()
        super().save(*args, **kwargs)


# =====================================================
# USER PROFILE (RBAC CORE)
# =====================================================

class UserProfile(BaseModel):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")

    roles = models.ManyToManyField(Role, blank=True)

    direct_permissions = models.ManyToManyField(Permission, blank=True)
    
    image = models.ImageField(
		upload_to=base_image_path,
		validators=[validate_image_extension],
		blank=True,
		null=True,
		help_text=_("Upload an image for the content."),
		verbose_name=_("Image"),
	)
    slug = models.SlugField(
		# unique=True,
		blank=True,
		null=True,
		help_text=_("Enter a slug for the content."),
		verbose_name=_("Slug")
	)
    company = models.ForeignKey(Company, null=True, blank=True, on_delete=models.SET_NULL)
    department = models.ForeignKey(Department, null=True, blank=True, on_delete=models.SET_NULL)
    job_title = models.ForeignKey(JobTitle, null=True, blank=True, on_delete=models.SET_NULL)

    disabled = models.BooleanField(default=False)

    properties = models.ManyToManyField("properties.Property", blank=True, related_name="users")

    # =============================
    # PERMISSION CACHE
    # =============================

    _perm_cache = None

    def _build_permission_cache(self):
        perms = set()

        perms.update(self.direct_permissions.values_list("code", flat=True))

        perms.update(
            Permission.objects.filter(roles__in=self.roles.all()).values_list("code", flat=True)
        )

        self._perm_cache = perms

    def has_permission(self, perm_code, property=None):

        if self.user.is_superuser or self.user.is_admin:
            return True

        if property and not self.properties.filter(id=property.id).exists():
            return False

        if self._perm_cache is None:
            self._build_permission_cache()

        return perm_code in self._perm_cache

    def clear_permission_cache(self):
        self._perm_cache = None

    def save(self, *args, **kwargs):
        if self.image and self.image.name:
            self.image = compress_image(self.image)

        if not self.pk and not self.slug:
            self.slug = slugify(f"{self.user.first_name}-{self.user.last_name}")

        super().save(*args, **kwargs)

        if self.user_id:
            should_be_active = not self.disabled
            if self.user.is_active != should_be_active:
                self.user.is_active = should_be_active
                self.user.save(update_fields=["is_active"])


# =====================================================
# SIGNALS (AUTO PROFILE + CACHE INVALIDATION)
# =====================================================

from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver


@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(m2m_changed, sender=UserProfile.roles.through)
@receiver(m2m_changed, sender=UserProfile.direct_permissions.through)
def clear_cache(sender, instance, **kwargs):
    instance.clear_permission_cache()


# =====================================================
# INDEXING (Performance)
# =====================================================

class MetaIndexes:
    indexes = [
        models.Index(fields=["email"]),
    ]

from django.core.exceptions import PermissionDenied
from properties.models import Property


class UserPropertyAccessMixin:
    property_kwarg = "property_id"

    def get_allowed_properties(self):
        user = self.request.user
        if user.is_superuser or getattr(user, "is_admin", False):
            return Property.objects.all()

        if not hasattr(user, "profile"):
            return Property.objects.none()

        return user.profile.properties.filter(is_deleted=False).distinct()

    def get_selected_property(self):
        property_id = self.kwargs.get(self.property_kwarg) or self.request.GET.get("property")
        allowed_properties = self.get_allowed_properties()

        if not allowed_properties.exists():
            return None

        if not property_id:
            return allowed_properties.first()

        prop = allowed_properties.filter(id=property_id).first()
        if not prop:
            raise PermissionDenied("You do not have access to this property.")
        return prop

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["allowed_properties"] = self.get_allowed_properties()
        context["selected_property"] = self.get_selected_property()
        return context


class Notification(models.Model):
    LEVEL_CHOICES = (
        ("info", "Info"),
        ("success", "Success"),
        ("warning", "Warning"),
        ("error", "Error"),
    )

    title = models.CharField(max_length=200)
    message = models.TextField()
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES, default="info")
    link = models.CharField(max_length=300, blank=True, null=True)
    alert = models.BooleanField(default=False)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_notifications"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    send_to_all = models.BooleanField(default=False)
    

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class NotificationRecipient(models.Model):
    notification = models.ForeignKey(
        Notification,
        on_delete=models.CASCADE,
        related_name="recipients"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notification_items"
    )
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("notification", "user")

    def __str__(self):
        return f"{self.user.email} - {self.notification.title}"

    def get_absolute_url(self):
        return reverse("accounts:notification_center")



























# # -----------------------------
# # Permission System
# # -----------------------------

# class PermissionGroup(models.Model):
#     # Admin
#     # Corporate
#     # Supervisor
#     # Staff
#     name = models.CharField(max_length=150, unique=True)

#     class Meta:
#         ordering = ["name"]

#     def __str__(self):
#         return self.name


# class Permission(models.Model):

#     # create_user
#     # edit_user
#     # assign_property
#     # view_user
#     # delete_user

#     code = models.CharField(max_length=100, unique=True)
#     name = models.CharField(max_length=150)

#     group = models.ForeignKey(
#         PermissionGroup,
#         on_delete=models.CASCADE,
#         related_name="permissions"
#     )

#     class Meta:
#         ordering = ["name"]

#     def __str__(self):
#         return self.name


# class Role(models.Model):

#     code = models.CharField(max_length=50, unique=True)
#     name = models.CharField(max_length=100)

#     description = models.TextField(blank=True)

#     permissions = models.ManyToManyField(
#         Permission,
#         blank=True,
#         related_name="roles"
#     )

#     is_admin_role = models.BooleanField(default=False)

#     class Meta:
#         ordering = ["name"]

#     def __str__(self):
#         return self.name


# # -----------------------------
# # Core Lookup Models
# # -----------------------------

# class Department(models.Model):
#     name = models.CharField(max_length=150, unique=True)

#     def __str__(self):
#         return self.name


# class JobTitle(models.Model):
#     name = models.CharField(max_length=150, unique=True)

#     class Meta:
#         verbose_name = "Job Title"
#         verbose_name_plural = "Job Titles"

#     def __str__(self):
#         return self.name


# class Company(models.Model):
#     name = models.CharField(max_length=150, unique=True)

#     class Meta:
#         verbose_name = "Company"
#         verbose_name_plural = "Companies"

#     def __str__(self):
#         return self.name


# # -----------------------------
# # Custom User
# # -----------------------------

# class UserManager(BaseUserManager):

#     def create_user(self, email, first_name="", last_name="", password=None, **extra_fields):

#         if not email:
#             raise ValueError("Users must have an email")

#         email = self.normalize_email(email)

#         user = self.model(
#             email=email,
#             first_name=first_name,
#             last_name=last_name,
#             **extra_fields
#         )

#         user.set_password(password)
#         user.save(using=self._db)

#         return user


#     def create_superuser(self, email, first_name="", last_name="", password=None, **extra_fields):

#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#         extra_fields.setdefault("is_admin", True)
#         extra_fields.setdefault("is_verified", True)

#         return self.create_user(email, first_name, last_name, password, **extra_fields)


# class CustomUser(AbstractBaseUser, PermissionsMixin):

#     id = models.UUIDField(
#         primary_key=True,
#         default=uuid.uuid4,
#         editable=False
#     )

#     email = models.EmailField(unique=True)
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     verify_code = models.TextField(null=True, blank=True)
#     is_verified = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_admin = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     created_at = models.DateTimeField(auto_now_add=True)
#     auth_id = models.TextField(null=True, blank=True)

#     USERNAME_FIELD = "email"
#     REQUIRED_FIELDS = ["first_name", "last_name"]

#     objects = UserManager()

#     def __str__(self):
#         return self.email


#     def tokens(self):
#         refresh = RefreshToken.for_user(self)
#         return {
#             "refresh": str(refresh),
#             "access": str(refresh.access_token),
#         }


# # -----------------------------
# # User Profile
# # -----------------------------

# class UserProfile(models.Model):

#     user = models.OneToOneField(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#         related_name="profile",
#     )

#     role = models.ForeignKey(
#         Role,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )
#     # roles = models.ManyToManyField(Role, blank=True)

#     company = models.ForeignKey(
#         Company,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )

#     # company = models.ForeignKey(Company)

#     department = models.ForeignKey(
#         Department,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )

#     job_title = models.ForeignKey(
#         JobTitle,
#         on_delete=models.SET_NULL,
#         null=True,
#         blank=True
#     )

#     disabled = models.BooleanField(default=False)

#     properties = models.ManyToManyField(
#         "properties.Property",
#         blank=True,
#         related_name="users"
#     )

#     def has_permission(self, perm_code, property=None):

#         if self.user.is_superuser:
#             return True

#         if property and not self.properties.filter(id=property.id).exists():
#             return False

#         if self.direct_permissions.filter(code=perm_code).exists():
#             return True

#         return self.roles.filter(
#             permissions__code=perm_code
#         ).exists()


#     def save(self, *args, **kwargs):

#         super().save(*args, **kwargs)

#         should_be_active = not self.disabled

#         if self.user.is_active != should_be_active:
#             self.user.is_active = should_be_active
#             self.user.save(update_fields=["is_active"])