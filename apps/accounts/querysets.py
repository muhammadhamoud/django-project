from .models import CustomUser

def user_visibility_queryset(request):

    qs = CustomUser.objects.select_related(
        "profile",
        "profile__role",
        "profile__company",
        "profile__department"
    ).prefetch_related(
        "profile__properties"
    )

    if request.user.is_superuser:
        return qs

    if not hasattr(request.user, "profile"):
        return qs.none()

    profile = request.user.profile

    if profile.has_permission("view_user"):

        return qs.filter(
            profile__properties__in=profile.properties.all()
        ).distinct()

    return qs.none()