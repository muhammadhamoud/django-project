from django.contrib import admin
from parler.admin import TranslatableAdmin, TranslatableTabularInline, TranslatableStackedInline
from parler.admin import SortedRelatedFieldListFilter
from .models import SiteInformation, SiteInformationAdditional, SiteMetaData, Marketing, Service, Feature, BusinessCategory, Offering, Project, TeamMember, Testimonial, Framework, MenuItem

# Define the get_prepopulated_fields method for all inline classes
def get_prepopulated_fields(self, request, obj=None):
    return {'slug': ('name',)}

class SiteMetaDataInline(admin.StackedInline):
    model = SiteMetaData
    extra = 0

    def get_max_num(self, request, obj=None, **kwargs):
        if obj and obj.sitemetadata:
            return 1
        return super().get_max_num(request, obj, **kwargs)

class SiteAdditionalInformationInline(TranslatableTabularInline):
    model = SiteInformationAdditional
    extra = 0

@admin.register(SiteInformation)
class SiteInformationAdmin(TranslatableAdmin):
    list_display = ["name", "is_published", "is_featured"]
    list_filter = ["is_published", "is_featured"]
    list_editable = ["is_published", "is_featured"]
    
    inlines = [
        SiteMetaDataInline,
        SiteAdditionalInformationInline,
    ]

@admin.register(Marketing)
class MarketingAdmin(TranslatableAdmin):
    list_display = ["name", "is_published", "is_featured"]
    list_filter = ["is_published", "is_featured"]
    list_editable = ["is_published", "is_featured"]
    get_prepopulated_fields = get_prepopulated_fields

@admin.register(Service)
class ServiceAdmin(TranslatableAdmin):
    list_display = ["name", "is_published", "is_featured"]
    list_filter = ["is_published", "is_featured"]
    list_editable = ["is_published", "is_featured"]
    get_prepopulated_fields = get_prepopulated_fields

@admin.register(Feature)
class FeatureAdmin(TranslatableAdmin):
    list_display = ["name", "is_published", "is_featured"]
    list_filter = ["is_published", "is_featured"]
    list_editable = ["is_published", "is_featured"]
    get_prepopulated_fields = get_prepopulated_fields

@admin.register(Framework)
class FrameworkAdmin(TranslatableAdmin):
    list_display = ["name", "is_published", "is_featured"]
    list_filter = ["is_published", "is_featured"]
    list_editable = ["is_published", "is_featured"]
    get_prepopulated_fields = get_prepopulated_fields

@admin.register(BusinessCategory)
class BusinessCategoryAdmin(TranslatableAdmin):
    list_display = ["name", "is_published", "is_featured"]
    list_filter = ["is_published", "is_featured"]
    list_editable = ["is_published", "is_featured"]
    get_prepopulated_fields = get_prepopulated_fields

@admin.register(Offering)
class OfferingAdmin(TranslatableAdmin):
    list_display = ["name", "is_published", "is_featured"]
    list_filter = ["is_published", "is_featured"]
    list_editable = ["is_published", "is_featured"]
    get_prepopulated_fields = get_prepopulated_fields

@admin.register(Project)
class ProjectAdmin(TranslatableAdmin):
    list_display = ["name", "is_published", "is_featured"]
    list_filter = ["is_published", "is_featured"]
    list_editable = ["is_published", "is_featured"]
    get_prepopulated_fields = get_prepopulated_fields

@admin.register(TeamMember)
class TeamMemberAdmin(TranslatableAdmin):
    list_display = ["name", "is_published", "is_featured"]
    list_filter = ["is_published", "is_featured"]
    list_editable = ["is_published", "is_featured"]
    get_prepopulated_fields = get_prepopulated_fields

@admin.register(Testimonial)
class TestimonialAdmin(TranslatableAdmin):
    list_display = ["name", "is_published", "is_featured"]
    list_filter = ["is_published", "is_featured"]
    list_editable = ["is_published", "is_featured"]
    get_prepopulated_fields = get_prepopulated_fields


@admin.register(MenuItem)
class MenuItemAdmin(TranslatableAdmin):
    list_display = ["name", "is_published", "is_featured"]
    list_filter = ["is_published", "is_featured"]
    list_editable = ["is_published", "is_featured"]
    get_prepopulated_fields = get_prepopulated_fields


class CustomAdminPage(admin.AdminSite):
    site_header = 'Custom Admin Page'

admin_site = CustomAdminPage(name='custom_admin')

from django.conf import settings
admin.site.site_header = f"{settings.WEBISTE_NAME.upper()} administration"