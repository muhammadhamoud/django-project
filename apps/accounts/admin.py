from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import (
    CustomUser,
    UserProfile,
    Department,
    JobTitle,
    Company,
    Role,
    Permission,
    PermissionGroup,
    RoleTemplate
)


# -----------------------------
# Custom Forms
# -----------------------------

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "last_name")


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = "__all__"


# -----------------------------
# Profile Inline
# -----------------------------

class UserProfileInline(admin.StackedInline):

    model = UserProfile
    can_delete = False
    fk_name = "user"

    filter_horizontal = ("roles", "direct_permissions", "properties")

    def formfield_for_manytomany(self, db_field, request, **kwargs):

        if db_field.name == "properties":

            if request.user.is_superuser:
                kwargs["queryset"] = db_field.related_model.objects.all()

            else:
                if hasattr(request.user, "profile"):

                    if request.user.profile.has_permission("property.assign"):
                        kwargs["queryset"] = request.user.profile.properties.all()
                    else:
                        kwargs["queryset"] = db_field.related_model.objects.none()

        return super().formfield_for_manytomany(db_field, request, **kwargs)


# -----------------------------
# Custom User Admin
# -----------------------------

@admin.register(CustomUser)
class UserAdmin(BaseUserAdmin):

    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    inlines = (UserProfileInline,)

    list_display = (
        "email",
        "first_name",
        "last_name",
        "get_roles",
        "get_department",
        "get_job_title",
        "get_company",
        "get_disabled",
        "is_staff",
        "is_verified",
    )

    list_filter = (
        "is_staff",
        "is_superuser",
        "is_active",
        "is_verified",
        "profile__company",
        "profile__department",
    )

    search_fields = (
        "email",
        "first_name",
        "last_name",
        "profile__company__name",
        "profile__job_title__name",
        "profile__department__name",
    )

    ordering = ("email",)

    fieldsets = (
        ("Login", {"fields": ("email", "password")}),

        ("Personal", {
            "fields": ("first_name", "last_name")
        }),

        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
                "is_verified",
                "groups",
                "user_permissions",
            )
        }),

        ("Dates", {
            "fields": ("last_login",)
        }),
    )

    add_fieldsets = (
        (
            "Create User",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                    "is_active",
                    "is_verified",
                ),
            },
        ),
    )

    filter_horizontal = ("groups", "user_permissions")

    # -----------------------------
    # Secure queryset
    # -----------------------------

    def get_queryset(self, request):

        qs = super().get_queryset(request).select_related(
            "profile"
        ).prefetch_related(
            "profile__roles",
            "profile__properties"
        )

        if request.user.is_superuser:
            return qs

        if not hasattr(request.user, "profile"):
            return qs.none()

        profile = request.user.profile

        if profile.has_permission("user.view"):
            return qs.filter(
                profile__properties__in=profile.properties.all()
            ).distinct()

        return qs.none()

    # -----------------------------
    # Profile helpers
    # -----------------------------

    def _get_profile(self, obj):
        return getattr(obj, "profile", None)

    @admin.display(description="Roles")
    def get_roles(self, obj):
        profile = self._get_profile(obj)
        if not profile:
            return "-"
        return ", ".join(profile.roles.values_list("name", flat=True)) or "-"

    @admin.display(description="Department")
    def get_department(self, obj):
        profile = self._get_profile(obj)
        return profile.department if profile else "-"

    @admin.display(description="Job Title")
    def get_job_title(self, obj):
        profile = self._get_profile(obj)
        return profile.job_title if profile else "-"

    @admin.display(description="Company")
    def get_company(self, obj):
        profile = self._get_profile(obj)
        return profile.company if profile else "-"

    @admin.display(boolean=True, description="Disabled")
    def get_disabled(self, obj):
        profile = self._get_profile(obj)
        return profile.disabled if profile else False


# -----------------------------
# RBAC Admin
# -----------------------------

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):

    list_display = ("code", "name", "company", "is_admin_role")
    search_fields = ("code", "name")
    list_filter = ("company", "is_admin_role")

    filter_horizontal = ("permissions",)


@admin.register(RoleTemplate)
class RoleTemplateAdmin(admin.ModelAdmin):

    list_display = ("name",)
    filter_horizontal = ("permissions",)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):

    list_display = ("code", "name", "group")
    list_filter = ("group",)
    search_fields = ("code", "name")


@admin.register(PermissionGroup)
class PermissionGroupAdmin(admin.ModelAdmin):

    list_display = ("name",)


# -----------------------------
# Lookup Tables
# -----------------------------

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)