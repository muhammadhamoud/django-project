from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required

from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import CustomUser
from utils import Util, EmailTemplates


from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.utils.encoding import smart_bytes, smart_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings

from accounts.models import CustomUser
from utils import Util


User = get_user_model()


# =====================================================
# REGISTER
# =====================================================

# def register_view(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         if not email or not password:
#             messages.error(request, "Email and password required")
#             return redirect("accounts:register")

#         if CustomUser.objects.filter(email=email).exists():
#             messages.error(request, "User already exists")
#             return redirect("accounts:register")

#         user = CustomUser.objects.create_user(email=email, password=password)

#         # Send verification email
#         token = RefreshToken.for_user(user).access_token
#         link = f"http://127.0.0.1:8000/verify-email/?token={token}"

#         email_body = EmailTemplates.email_verfication_template(user.email, link)

#         Util.send_email({
#             "to_email": user.email,
#             "email_body": email_body,
#             "email_subject": "Verify your email"
#         })

#         messages.success(request, "Account created. Check your email.")
#         return redirect("accounts:login")

#     return render(request, "accounts/register.html", {"homepage": True})


def submit_verification_email(request, user):
    token = RefreshToken.for_user(user).access_token
    path = reverse("accounts:verify_email")
    link = f"http://{request.get_host()}{path}?token={token}"

    email_body = EmailTemplates.email_verfication_template(user.email, link)

    Util.send_email({
        "to_email": user.email,
        "email_body": email_body,
        "email_subject": "Verify your email",
    })

    


# def register_view(request):
#     if request.method == "POST":
#         email = request.POST.get("email")
#         password = request.POST.get("password")

#         if not email or not password:
#             messages.error(request, "Email and password required")
#             return redirect("accounts:register")

#         if CustomUser.objects.filter(email=email).exists():
#             messages.error(request, "User already exists")
#             return redirect("accounts:register")

#         user = CustomUser.objects.create_user(email=email, password=password)

#         submit_verification_email(request, user)

#         messages.success(request, "Account created. Check your email.")
#         return redirect("accounts:login")

#     return render(request, "accounts/register.html", {"homepage": True})


def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        if not first_name or not last_name or not email or not password or not confirm_password:
            messages.error(request, "All fields are required.")
            return redirect("accounts:register")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("accounts:register")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "User already exists.")
            return redirect("accounts:register")

        user = CustomUser.objects.create_user(
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password,
        )

        submit_verification_email(request, user)

        messages.success(request, "Account created. Check your email.")
        return redirect("accounts:login")

    return render(request, "accounts/register.html", {"homepage": True})


def resend_verification_view(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()

        if not email:
            messages.error(request, "Email is required")
            return redirect("accounts:resend_verification")

        user = CustomUser.objects.filter(email=email).first()

        if not user:
            messages.error(request, "No account found with this email")
            return redirect("accounts:resend_verification")

        if user.is_verified:
            messages.info(request, "This email is already verified")
            return redirect("accounts:login")

        submit_verification_email(request, user)

        messages.success(request, "Verification email sent successfully")
        return redirect("accounts:login")

    return render(request, "accounts/resend_verification.html", {
        "homepage": True,
    })


from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError

def verify_email_view(request):
    token = request.GET.get("token")

    if not token:
        messages.error(request, "Verification token is missing.")
        return redirect("accounts:login")

    try:
        access_token = AccessToken(token)
        user_id = access_token["user_id"]
        user = CustomUser.objects.get(id=user_id)

        if not user.is_verified:
            user.is_verified = True
            user.save(update_fields=["is_verified"])

        messages.success(request, "Email verified successfully. You can now log in.")
        return redirect("accounts:login")

    except TokenError:
        messages.error(request, "Invalid or expired verification token.")
        return redirect("accounts:login")

    except CustomUser.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("accounts:login")

# =====================================================
# LOGIN
# =====================================================

def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)

        if not user:
            messages.error(request, "Invalid credentials")
            return redirect("accounts:login")

        if not user.is_verified:
            messages.error(request, "Email not verified")
            return redirect("accounts:login")

        login(request, user)
        return redirect("dashboard:home")

    return render(request, "accounts/login.html", {"homepage": True})


# =====================================================
# LOGOUT
# =====================================================

def logout_view(request):
    logout(request)
    return redirect("accounts:login")



def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if not CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email not found")
            return redirect("accounts:forgot_password")

        user = CustomUser.objects.get(email=email)

        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        link = reverse("accounts:reset_password", kwargs={
            "uidb64": uidb64,
            "token": token
        })

        reset_url = f"http://{request.get_host()}{link}"

        # Send email
        Util.send_email({
            "to_email": user.email,
            "email_body": f"Click to reset your password:\n{reset_url}",
            "email_subject": "Reset Password"
        })

        messages.success(request, "Password reset link sent to your email")
        return redirect("accounts:login")

    return render(request, "accounts/forgot_password.html", {"homepage": True})


def reset_password_view(request, uidb64, token):
    try:
        user_id = smart_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(id=user_id)
    except Exception:
        messages.error(request, "Invalid reset link")
        return redirect("accounts:login")

    # Check token validity
    if not PasswordResetTokenGenerator().check_token(user, token):
        messages.error(request, "Invalid or expired token")
        return redirect("accounts:login")

    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if not password:
            messages.error(request, "Password is required")
            return redirect(request.path)

        if password != confirm_password:
            messages.error(request, "Passwords do not match")

        user.set_password(password)
        user.save()

        messages.success(request, "Password reset successful. Please login.")
        return redirect("accounts:login")

    return render(request, "accounts/reset_password.html", {
        "uidb64": uidb64,
        "token": token,
        "homepage": True,
    })


# =====================================================
# DASHBOARD / CURRENT USER
# =====================================================

# @login_required
# def dashboard_view(request):
#     apps = [
#         {"name": "Revenue", "icon": "fa-chart-line", "color": "blue", "report_id": "REPORT_ID_1"},
#         {"name": "Occupancy", "icon": "fa-bed", "color": "green", "report_id": "REPORT_ID_2"},
#         {"name": "Distribution", "icon": "fa-globe", "color": "purple", "report_id": "REPORT_ID_3"},
#         {"name": "Guests", "icon": "fa-users", "color": "orange", "report_id": "REPORT_ID_4"},
#         {"name": "Reputation", "icon": "fa-star", "color": "yellow", "report_id": "REPORT_ID_5"},
#         {"name": "F&B", "icon": "fa-utensils", "color": "red", "report_id": "REPORT_ID_6"},
#         {"name": "Operations", "icon": "fa-cogs", "color": "gray", "report_id": "REPORT_ID_7"},
#         {"name": "Marketing", "icon": "fa-bullhorn", "color": "pink", "report_id": "REPORT_ID_8"},
#         {"name": "Corporate", "icon": "fa-building", "color": "indigo", "report_id": "REPORT_ID_9"},
#         {"name": "Forecast", "icon": "fa-chart-area", "color": "teal", "report_id": "REPORT_ID_10"},
#         {"name": "Market", "icon": "fa-chart-pie", "color": "cyan", "report_id": "REPORT_ID_11"},
#         {"name": "Tech", "icon": "fa-microchip", "color": "slate", "report_id": "REPORT_ID_12"},
#     ]
#     return render(request, "dashboard.html", {"apps": apps})


# def powerbi_report(request, report_id):
#     return render(request, "report.html", {
#         "report_id": report_id
#     })




# =====================================================
# USERS LIST
# =====================================================

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from accounts.models import CustomUser, UserProfile
from django.shortcuts import redirect, render
from accounts.permissions import permission_required, property_permission_required

@login_required
def user_list_view(request):
    if not permission_required("user.view")().has_permission(request, None):
        messages.error(request, "Permission denied")
        return redirect("dashboard:home")

    user = request.user
    profile = user.profile

    if not (
        profile.roles.filter(code="supervisor").exists()
        or profile.roles.filter(code="super_admin").exists()
    ):
        messages.error(request, "Only supervisors can view users")
        return redirect("dashboard:home")

    users = CustomUser.objects.filter(
        profile__properties__in=profile.properties.all()
    ).distinct()

    email = request.GET.get("email", "").strip()
    first_name = request.GET.get("first_name", "").strip()
    last_name = request.GET.get("last_name", "").strip()
    company = request.GET.get("company", "").strip()
    department = request.GET.get("department", "").strip()
    job_title = request.GET.get("job_title", "").strip()
    role = request.GET.get("role", "").strip()
    disabled = request.GET.get("disabled", "").strip()

    if email:
        users = users.filter(email__icontains=email)

    if first_name:
        users = users.filter(first_name__icontains=first_name)

    if last_name:
        users = users.filter(last_name__icontains=last_name)

    if company:
        users = users.filter(profile__company__name__icontains=company)

    if department:
        users = users.filter(profile__department__name__icontains=department)

    if job_title:
        users = users.filter(profile__job_title__icontains=job_title)

    if role:
        users = users.filter(profile__roles__name__icontains=role)

    if disabled == "yes":
        users = users.filter(is_active=False)
    elif disabled == "no":
        users = users.filter(is_active=True)

    users = users.order_by("first_name", "last_name", "email").distinct()

    allowed_page_sizes = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]

    try:
        page_size = int(request.GET.get("page_size", 10))
    except (TypeError, ValueError):
        page_size = 10

    if page_size not in allowed_page_sizes:
        page_size = 10

    paginator = Paginator(users, page_size)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        "page_obj": page_obj,
        "page_size": page_size,
        "allowed_page_sizes": allowed_page_sizes,
        "filters": {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "company": company,
            "department": department,
            "job_title": job_title,
            "role": role,
            "disabled": disabled,
        },
    }

    return render(request, "accounts/user_list.html", context)


# =====================================================
# USER DETAILS
# =====================================================

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages

from properties.models import Property
from .models import CustomUser, Company, Department, JobTitle, Role, Permission

@login_required
def user_detail_view(request, id):
    if not permission_required("user.view")().has_permission(request, None):
        messages.error(request, "Permission denied")
        return redirect("accounts:user_list")

    user = get_object_or_404(
        CustomUser.objects.filter(
            profile__properties__in=request.user.profile.properties.all()
        ).distinct(),
        id=id
    )

    profile = user.profile
    available_properties = request.user.profile.properties.all()
    can_edit = permission_required("user.edit")().has_permission(request, None)

    if request.method == "POST":
        if not can_edit:
            messages.error(request, "Permission denied")
            return redirect("accounts:user_list")

        user.first_name = request.POST.get("first_name", user.first_name)
        user.last_name = request.POST.get("last_name", user.last_name)
        user.save()

        profile.company_id = request.POST.get("company") or None
        profile.department_id = request.POST.get("department") or None
        profile.job_title_id = request.POST.get("job_title") or None
        profile.disabled = request.POST.get("disabled") == "on"

        role_ids = request.POST.getlist("roles")
        profile.roles.set(role_ids)

        selected_properties = request.POST.getlist("properties")
        allowed_ids = available_properties.values_list("id", flat=True)

        properties = Property.objects.filter(
            id__in=selected_properties
        ).filter(
            id__in=allowed_ids
        )

        profile.properties.set(properties)
        profile.save()

        messages.success(request, "User updated successfully")
        return redirect("accounts:user_detail", id=str(user.id))

    return render(request, "accounts/user_detail.html", {
        "user_obj": user,
        "profile": profile,
        "available_properties": available_properties,
        "assigned_properties": profile.properties.all(),
        "companies": Company.objects.all(),
        "departments": Department.objects.all(),
        "job_titles": JobTitle.objects.all(),
        "roles": Role.objects.all(),
        "can_edit": can_edit,
    })


# @login_required
# def user_detail_view(request, id):

#     # 🔐 View permission
#     if not permission_required("user.view")().has_permission(request, None):
#         messages.error(request, "Permission denied")
#         return redirect("user_list")

#     user = get_object_or_404(
#         CustomUser.objects.filter(
#             profile__properties__in=request.user.profile.properties.all()
#         ).distinct(),
#         id=id
#     )

#     profile = user.profile

#     # ✅ Properties current user can assign
#     available_properties = request.user.profile.properties.all()

#     if request.method == "POST":

#         # 🔐 Edit permission
#         if not permission_required("user.edit")().has_permission(request, None):
#             messages.error(request, "Permission denied")
#             return redirect("user_list")

#         # =========================
#         # USER (NO EMAIL UPDATE ❌)
#         # =========================
#         user.first_name = request.POST.get("first_name", user.first_name)
#         user.last_name = request.POST.get("last_name", user.last_name)
#         user.save()

#         # =========================
#         # PROFILE UPDATE
#         # =========================
#         profile.company_id = request.POST.get("company") or None
#         profile.department_id = request.POST.get("department") or None
#         profile.job_title_id = request.POST.get("job_title") or None
#         profile.disabled = request.POST.get("disabled") == "on"

#         # =========================
#         # ROLES
#         # =========================
#         role_ids = request.POST.getlist("roles")
#         if role_ids:
#             profile.roles.set(role_ids)

#         # =========================
#         # DIRECT PERMISSIONS
#         # =========================
#         # permission_ids = request.POST.getlist("direct_permissions")
#         # if permission_ids:
#         #     profile.direct_permissions.set(permission_ids)

#         # =========================
#         # PROPERTIES (SAFE FILTER)
#         # =========================
#         selected_properties = request.POST.getlist("properties")

#         allowed_ids = available_properties.values_list("id", flat=True)

#         properties = Property.objects.filter(
#             id__in=selected_properties
#         ).filter(
#             id__in=allowed_ids
#         )

#         profile.properties.set(properties)

#         profile.save()

#         messages.success(request, "User updated successfully")
#         return redirect("user_detail", id=user.id)

#     # =========================
#     # GET CONTEXT
#     # =========================
#     return render(request, "user_detail.html", {
#         "user_obj": user,
#         "profile": profile,
#         "available_properties": available_properties,
#         "assigned_properties": profile.properties.all(),

#         # Optional (for dropdowns)
#         "companies": Company.objects.all(),
#         "departments": Department.objects.all(),
#         "job_titles": JobTitle.objects.all(),
#         "roles": Role.objects.all(),
#         # "permissions": Permission.objects.all(),
#     })


# =====================================================
# CURRENT USER
# =====================================================

@login_required
def current_user_view(request):
    return render(request, "accounts/current_user.html", {
        "user": request.user
    })


# =====================================================
# PROFILE
# =====================================================
from django.contrib.auth.forms import PasswordChangeForm


@login_required
def profile_view(request):
    user = request.user
    profile = user.profile

    if request.method == "POST":
        form_type = request.POST.get("form_type")

        if form_type == "profile":
            first_name = request.POST.get("first_name", "").strip()
            last_name = request.POST.get("last_name", "").strip()

            company_id = request.POST.get("company") or None
            department_id = request.POST.get("department") or None
            job_title_id = request.POST.get("job_title") or None

            if not first_name or not last_name:
                messages.error(request, "First name and last name are required.")
                return redirect("accounts:profile")

            user.first_name = first_name
            user.last_name = last_name
            user.save()

            profile.company_id = company_id
            profile.department_id = department_id
            profile.job_title_id = job_title_id
            profile.save()

            messages.success(request, "Profile updated successfully.")
            return redirect("accounts:profile")

        elif form_type == "password":
            password_form = PasswordChangeForm(user, request.POST)

            if password_form.is_valid():
                updated_user = password_form.save()
                update_session_auth_hash(request, updated_user)
                messages.success(request, "Password changed successfully.")
                return redirect("accounts:profile")

            messages.error(request, "Please correct the password form errors.")
        else:
            password_form = PasswordChangeForm(user)

    else:
        password_form = PasswordChangeForm(user)

    context = {
        "profile_obj": profile,
        "password_form": password_form,
        "companies": Company.objects.all(),
        "departments": Department.objects.all(),
        "job_titles": JobTitle.objects.all(),
    }
    return render(request, "accounts/profile.html", context)