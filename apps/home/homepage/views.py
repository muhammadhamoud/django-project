from django.http import Http404
from django.shortcuts import render, get_object_or_404
from datetime import datetime as dt
from django.conf import settings
from .models import *
# Create your views here.

# Define your API views
from django.http import HttpResponseRedirect
def api_view(request):
    # Redirect to the specific site
    return HttpResponseRedirect('https://hamouds.com')


def index(request):
    import os
    # List of JavaScript filenames
    # Path to your static folder
    static_folder = os.path.join(settings.BASE_DIR, "static")

    # List of JavaScript filenames from the static folder
    js_files = [f for f in os.listdir(static_folder) if f.endswith('.js')]
    # print(js_files)
    context = {
        "js_files": js_files,
    }
    return render(request, 'homepage/index.html', context)


def home(request):
    # info = SiteInformation.objects.all()
    # if len(info) != 1:
    #     raise Http404('Information for this site is not posted.')
    # info = info[0]

    offerings = Offering.objects.all().order_by('-is_featured')
    services = Service.objects.all().order_by('-is_featured')
    projects = Project.objects.filter(is_published=True).order_by('-modified')
    features = Feature.objects.all().order_by('-is_featured')
    marketings = Marketing.objects.all().order_by('-is_featured')
    teammembers = TeamMember.objects.all().order_by('-is_featured')
    testimonials = Testimonial.objects.all().order_by('-is_featured')

    site = SiteInformation.objects.filter(is_published=True).first()
    navbar_menu = MenuItem.objects.filter(
         site=site,
        parent__isnull=True,
        is_published=True
    ).prefetch_related('children')

    pricing_section = (
        PricingSection.objects
        .filter(is_published=True)
        .prefetch_related('plans', 'plans__features', 'plans__limits')
        .order_by('-created')
        .first()
    )

    pricing_plans = (
        pricing_section.plans.filter(is_published=True).order_by('sort_order', 'id')
        if pricing_section else []
    )


    context = {
        # 'site_information': info,
        'services': services,
        'projects': projects,
        'features': features,
        'offerings': offerings,
        'marketings': marketings,
        'teammembers': teammembers,
        'testimonials': testimonials,
        'navbar_menu': navbar_menu,
        'copyright': f'2000-{dt.now().year}',
        "homepage": True,	
        'pricing_section': pricing_section,
        'pricing_plans': pricing_plans,
    }
    return render(request, 'homepage/base.html', context)


def offering_detail(request, slug):
    offering = get_object_or_404(Offering, slug=slug)
    return render(request, 'homepage/offering_detail.html', {'offering': offering})

def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    return render(request, 'homepage/service_detail.html', {'service': service})

def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)
    return render(request, 'homepage/project_detail.html', {'project': project})

def feature_detail(request, slug):
    feature = get_object_or_404(Feature, slug=slug)
    return render(request, 'homepage/feature_detail.html', {'feature': feature})

def framework_detail(request, slug):
    framework = get_object_or_404(Framework, slug=slug)
    return render(request, 'homepage/framework_detail.html', {'framework': framework})

def marketing_detail(request, slug):
    marketing = get_object_or_404(Marketing, slug=slug)
    return render(request, 'homepage/marketing_detail.html', {'marketing': marketing})

def business_category_detail(request, slug):
    category = get_object_or_404(BusinessCategory, slug=slug)
    return render(request, 'homepage/business_category_detail.html', {'category': category})

def teammember_detail(request, slug):
    member = get_object_or_404(TeamMember, slug=slug)
    return render(request, 'homepage/teammember_detail.html', {'member': member})

def testimonial_detail(request, slug):
    testimonial = get_object_or_404(Testimonial, slug=slug)
    return render(request, 'homepage/testimonial_detail.html', {'testimonial': testimonial})


def _get_site_additional():
    site = SiteInformation.objects.filter(is_published=True).first()
    if not site:
        return None, None

    additional = SiteInformationAdditional.objects.filter(site=site).first()
    return site, additional


def about_us_view(request):
    site, additional = _get_site_additional()
    return render(request, "homepage/about_us.html", {
        "site_information": site,
        "site_additional": additional,
        "homepage": True,
    })


def privacy_policy_view(request):
    site, additional = _get_site_additional()
    return render(request, "homepage/privacy_policy.html", {
        "site_information": site,
        "site_additional": additional,
        "homepage": True,
    })


def terms_of_service_view(request):
    site, additional = _get_site_additional()
    return render(request, "homepage/terms_of_service.html", {
        "site_information": site,
        "site_additional": additional,
        "homepage": True,
    })


from django.shortcuts import render, get_object_or_404

from .models import PricingSection, PricingPlan


def pricing_section_list(request):
    pricing_sections = (
        PricingSection.objects
        .filter(is_published=True)
        .select_related('site')
        .prefetch_related('plans')
        .order_by('-created')
    )

    context = {
        'pricing_sections': pricing_sections,
        'page_title': 'Pricing',
        'page_subtitle': 'Choose the plan that fits your business needs.',
        'homepage': True,
    }
    return render(request, 'homepage/pricing/pricing_section_list.html', context)


def pricing_section_detail(request, slug):
    pricing_section = get_object_or_404(
        PricingSection.objects
        .filter(is_published=True)
        .select_related('site')
        .prefetch_related('plans', 'plans__features', 'plans__limits'),
        slug=slug
    )

    plans = (
        pricing_section.plans
        .filter(is_published=True)
        .prefetch_related('features', 'limits')
        .order_by('sort_order', 'id')
    )

    # featured_plan = plans.filter(is_featured=True).first()
    print(plans)
    context = {
        'pricing_section': pricing_section,
        'plans': plans,
        # 'featured_plan': featured_plan,
        'page_title': pricing_section.name,
        'page_subtitle': pricing_section.description,
        'homepage': True,
    }
    return render(request, 'homepage/pricing/pricing_section_detail.html', context)


def pricing_plan_detail(request, slug):
    plan = get_object_or_404(
        PricingPlan.objects
        .filter(is_published=True, section__is_published=True)
        .select_related('section', 'section__site')
        .prefetch_related('features', 'limits')
        .order_by('sort_order', 'id'),
        slug=slug
    )

    related_plans = (
        PricingPlan.objects
        .filter(
            section=plan.section,
            is_published=True
        )
        .exclude(id=plan.id)
        .order_by('sort_order', 'id')
    )

    features = plan.features.filter(is_published=True).order_by('sort_order', 'id')
    limits = plan.limits.filter(is_published=True).order_by('sort_order', 'id')

    context = {
        'plan': plan,
        'features': features,
        'limits': limits,
        'related_plans': related_plans,
        'pricing_section': plan.section,
        'page_title': plan.name,
        'page_subtitle': getattr(plan, 'short_description', '') or plan.description,
        'homepage': True,
    }
    return render(request, 'homepage/pricing/pricing_plan_detail.html', context)


def pricing_comparison(request, slug):
    pricing_section = get_object_or_404(
        PricingSection.objects.filter(is_published=True),
        slug=slug
    )

    plans = (
        pricing_section.plans
        .filter(is_published=True)
        .prefetch_related('features', 'limits')
        .order_by('sort_order', 'id')
    )

    context = {
        'pricing_section': pricing_section,
        'plans': plans,
        'page_title': f'{pricing_section.name} Comparison',
        'page_subtitle': pricing_section.description,
        'homepage': True,
    }
    return render(request, 'homepage/pricing/pricing_comparison.html', context)


# from django.shortcuts import get_object_or_404
# from django.views.generic import ListView, DetailView, TemplateView

# from .models import (
#     PricingSection,
#     PricingPlan,
# )


# class PricingSectionListView(ListView):
#     """
#     Show all published pricing sections.
#     Useful if the website may have more than one pricing section/page.
#     """
#     model = PricingSection
#     template_name = 'homepage/pricing/pricing_section_list.html'
#     context_object_name = 'pricing_sections'

#     def get_queryset(self):
#         return (
#             PricingSection.objects
#             .filter(is_published=True)
#             .select_related('site')
#             .prefetch_related('plans')
#             .order_by('-created')
#         )

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['page_title'] = 'Pricing'
#         context['page_subtitle'] = 'Choose the plan that fits your business needs.'
#         context["homepage"] =True
#         return context


# class PricingSectionDetailView(DetailView):
#     """
#     Main pricing page.
#     Shows one pricing section and all related plans, features, and limits.
#     """
#     model = PricingSection
#     template_name = 'homepage/pricing/pricing_section_detail.html'
#     context_object_name = 'pricing_section'
#     slug_field = 'slug'
#     slug_url_kwarg = 'slug'

#     def get_queryset(self):
#         return (
#             PricingSection.objects
#             .filter(is_published=True)
#             .select_related('site')
#             .prefetch_related(
#                 'plans',
#                 'plans__features',
#                 'plans__limits',
#             )
#         )

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         plans = (
#             self.object.plans
#             .filter(is_published=True)
#             .prefetch_related('features', 'limits')
#             .order_by('sort_order', 'id')
#         )

#         featured_plan = plans.filter(is_featured=True).first()

#         context['plans'] = plans
#         context['featured_plan'] = featured_plan
#         context['page_title'] = self.object.name
#         context['page_subtitle'] = self.object.description
#         context["homepage"] =True

#         return context


# class PricingPlanDetailView(DetailView):
#     """
#     Single pricing plan detail page.
#     Good for CTA buttons like 'Learn More' or dedicated plan pages.
#     """
#     model = PricingPlan
#     template_name = 'homepage/pricing/pricing_plan_detail.html'
#     context_object_name = 'plan'
#     slug_field = 'slug'
#     slug_url_kwarg = 'slug'

#     def get_queryset(self):
#         return (
#             PricingPlan.objects
#             .filter(is_published=True, section__is_published=True)
#             .select_related('section', 'section__site')
#             .prefetch_related('features', 'limits')
#             .order_by('sort_order', 'id')
#         )

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         related_plans = (
#             PricingPlan.objects
#             .filter(
#                 section=self.object.section,
#                 is_published=True
#             )
#             .exclude(id=self.object.id)
#             .order_by('sort_order', 'id')
#         )

#         context['features'] = self.object.features.filter(is_published=True).order_by('sort_order', 'id')
#         context['limits'] = self.object.limits.filter(is_published=True).order_by('sort_order', 'id')
#         context['related_plans'] = related_plans
#         context['pricing_section'] = self.object.section
#         context['page_title'] = self.object.name
#         context['page_subtitle'] = self.object.short_description or self.object.description
#         context["homepage"] =True

#         return context


# class PricingComparisonView(TemplateView):
#     """
#     Optional comparison page for all plans under one section.
#     Great for Tailwind pricing comparison tables.
#     """
#     template_name = 'homepage/pricing/pricing_comparison.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)

#         slug = self.kwargs.get('slug')
#         pricing_section = get_object_or_404(
#             PricingSection.objects.filter(is_published=True),
#             slug=slug
#         )

#         plans = (
#             pricing_section.plans
#             .filter(is_published=True)
#             .prefetch_related('features', 'limits')
#             .order_by('sort_order', 'id')
#         )

#         context['pricing_section'] = pricing_section
#         context['plans'] = plans
#         context['page_title'] = f'{pricing_section.name} Comparison'
#         context['page_subtitle'] = pricing_section.description
#         context["homepage"] =True

#         return context

