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
    return render(request, 'homepage/main.html', context)


def home(request):
    # info = SiteInformation.objects.all()
    # if len(info) != 1:
    #     raise Http404('Information for this site is not posted.')
    # info = info[0]

    offerings = Offering.objects.all()
    services = Service.objects.all()
    projects = Project.objects.filter(is_published=True).order_by('-modified')
    features = Feature.objects.all()
    marketings = Marketing.objects.all()
    teammembers = TeamMember.objects.all()
    testimonials = Testimonial.objects.all()

    site = SiteInformation.objects.filter(is_published=True).first()
    navbar_menu = MenuItem.objects.filter(
         site=site,
        parent__isnull=True,
        is_published=True
    ).prefetch_related('children')

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
    }
    return render(request, 'homepage/main.html', context)


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