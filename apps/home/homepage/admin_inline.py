from django.contrib import admin
from parler.admin import TranslatableAdmin, TranslatableTabularInline, TranslatableStackedInline
from parler.admin import SortedRelatedFieldListFilter

# class Projectdmin(admin.ModelAdmin):
#     list_display = ('name', 'is_published')  # Include 'is_published' in the list of displayed fields

from django.contrib import admin
from .models import SiteInformation, SiteInformationAdditional, SiteMetaData, Marketing, Service, Feature, BusinessCategory, Offering, Project, TeamMember, Testimonial

# from django import forms
# class SiteInformationForm(forms.ModelForm):
#     class Meta:
#         model = SiteInformation
#         fields = '__all__'

# Define the get_prepopulated_fields method for all inline classes
def get_prepopulated_fields(self, request, obj=None):
    return {'slug': ('name',)}

class SiteMetaDataInline(admin.StackedInline):
    model = SiteMetaData
    extra = 0

    def get_max_num(self, request, obj=None, **kwargs):
        # Check if there's an existing SiteMetaData for this site
        if obj and obj.sitemetadata:
            # If there's an existing SiteMetaData, allow only one entry
            return 1
        # Otherwise, allow creation of a new SiteMetaData
        return super().get_max_num(request, obj, **kwargs)

class SiteAdditionalInformationInline(TranslatableTabularInline):
    model = SiteInformationAdditional
    extra = 0

# Inline admin classes for related models
class MarketingInline(TranslatableTabularInline):
    model = Marketing
    extra = 0
    def get_prepopulated_fields(self, request, obj=None):
        return {'slug': ('name',)}

class ServiceInline(TranslatableTabularInline):
    model = Service
    extra = 0
    get_prepopulated_fields = get_prepopulated_fields

class FeatureInline(TranslatableTabularInline):
    model = Feature
    extra = 0
    get_prepopulated_fields = get_prepopulated_fields

class BsuinessCategoryInline(TranslatableTabularInline):
    model = BusinessCategory
    extra = 0
    get_prepopulated_fields = get_prepopulated_fields

class OfferingInline(TranslatableTabularInline):
    model = Offering
    extra = 0
    get_prepopulated_fields = get_prepopulated_fields

class ProjectInline(TranslatableStackedInline):
    model = Project
    extra = 0
    get_prepopulated_fields = get_prepopulated_fields

class TeamMemberInline(TranslatableStackedInline):
    model = TeamMember
    extra = 0
    get_prepopulated_fields = get_prepopulated_fields

class TestimonialInline(TranslatableStackedInline):
    model = Testimonial
    extra = 0
    get_prepopulated_fields = get_prepopulated_fields

# Main admin class for SiteInformation
# @admin.register(SiteInformation)

@admin.register(SiteInformation)
class SiteInformationAdmin(TranslatableAdmin):

    # translated_fields  = ['site_name', 'company_name', 'site_description', 'site_keywords', 'tagline']
    # list_display = ['get_translated_field']

    inlines = [
        SiteMetaDataInline,
        SiteAdditionalInformationInline,
        MarketingInline,
        ServiceInline,
        FeatureInline,
        BsuinessCategoryInline,
        OfferingInline,
        ProjectInline,
        TeamMemberInline,
        TestimonialInline,
        ]


    # list_filter = (
    #         ('related_field_name', SortedRelatedFieldListFilter),
    #     )

# @admin.register(Marketing)
# class MarketingnAdmin(TranslatableAdmin):
#     pass
    # # readonly_fields = ["site"]
    # list_display = ['name', 'slug']
    # ordering = ["-modified"]
    # search_fields = ["translations__name", "translations__description"]

    # def get_prepopulated_fields(self, request, obj=None):
    #     return {'slug': ('name',)}

# @admin.register(AdditionalSiteInformation)
# class AdditionalInformationAdmin(TranslatableAdmin):
#     pass


class CustomAdminPage(admin.AdminSite):
    site_header = 'Custom Admin Page'

admin_site = CustomAdminPage(name='custom_admin')

from django.conf import settings
admin.site.site_header = f"{settings.WEBISTE_NAME.upper()} administration"


