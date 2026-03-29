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




# from django.contrib import admin
# from parler.admin import TranslatableAdmin, TranslatableStackedInline

from .models import (
	PricingSection,
	PricingPlan,
	PricingFeature,
	PricingPlanLimit,
)


class PricingFeatureInline(TranslatableStackedInline):
	model = PricingFeature
	extra = 1
	fields = (
		'name',
		'description',
		'value_type',
		'value_text',
		'value_boolean',
		'value_number',
		'sort_order',
		'is_published',
	)
	ordering = ('sort_order', 'id')


class PricingPlanLimitInline(TranslatableStackedInline):
	model = PricingPlanLimit
	extra = 1
	fields = (
		'name',
		'unit',
		'limit_type',
		'custom_value',
		'value_integer',
		'value_decimal',
		'sort_order',
		'is_published',
	)
	ordering = ('sort_order', 'id')


class PricingPlanInline(TranslatableStackedInline):
	model = PricingPlan
	extra = 1
	fields = (
		'name',
		'short_description',
		'description',
		'badge_text',
		'price_label',
		'button_text',
		'button_url',
		'billing_interval',
		'currency',
		'price',
		'compare_at_price',
		'setup_fee',
		'trial_days',
		'is_free',
		'is_custom_price',
		'allow_subscribe',
		'allow_contact_sales',
		'is_featured',
		'is_published',
		'sort_order',
	)
	ordering = ('sort_order', 'id')
	show_change_link = True


@admin.register(PricingSection)
class PricingSectionAdmin(TranslatableAdmin):
	list_display = ('__str__', 'site', 'is_featured', 'is_published', 'created')
	list_filter = ('site', 'is_featured', 'is_published', 'created')
	search_fields = ('translations__name', 'translations__description')
	prepopulated_fields = {}
	inlines = [PricingPlanInline]


@admin.register(PricingPlan)
class PricingPlanAdmin(TranslatableAdmin):
	list_display = (
		'__str__',
		'section',
		'billing_interval',
		'currency',
		'price',
		'is_free',
		'is_custom_price',
		'is_featured',
		'is_published',
		'sort_order',
	)
	list_filter = (
		'billing_interval',
		'currency',
		'is_free',
		'is_custom_price',
		'is_featured',
		'is_published',
	)
	search_fields = (
		'translations__name',
		'translations__description',
		'translations__short_description',
	)
	inlines = [PricingFeatureInline, PricingPlanLimitInline]


@admin.register(PricingFeature)
class PricingFeatureAdmin(TranslatableAdmin):
	list_display = (
		'__str__',
		'plan',
		'value_type',
		'display_value',
		'is_featured',
		'is_published',
		'sort_order',
	)
	list_filter = (
		'value_type',
		'is_featured',
		'is_published',
	)
	search_fields = (
		'translations__name',
		'translations__description',
		'translations__value_text',
	)


@admin.register(PricingPlanLimit)
class PricingPlanLimitAdmin(TranslatableAdmin):
	list_display = (
		'__str__',
		'plan',
		'limit_type',
		'display_limit',
		'is_featured',
		'is_published',
		'sort_order',
	)
	list_filter = (
		'limit_type',
		'is_featured',
		'is_published',
	)
	search_fields = (
		'translations__name',
		'translations__unit',
		'translations__custom_value',
	)
