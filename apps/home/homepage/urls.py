from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from . import views


app_name = "homepage"
urlpatterns = [
    path('', views.home, name='home'),

    path('services/<slug:slug>/', views.service_detail, name='service-detail'),
    path("offerings/<slug:slug>/", views.offering_detail, name="offering-detail"),
    path('projects/<slug:slug>/', views.project_detail, name='project-detail'),
    path('features/<slug:slug>/', views.feature_detail, name='feature-detail'),
    path('frameworks/<slug:slug>/', views.framework_detail, name='framework-detail'),
    path('marketing/<slug:slug>/', views.marketing_detail, name='marketing-detail'),
    path('categories/<slug:slug>/', views.business_category_detail, name='product-category-detail'),
    path('team/<slug:slug>/', views.teammember_detail, name='teammember-detail'),
    path('testimonials/<slug:slug>/', views.testimonial_detail, name='testimonial-detail'),

    # TODO fix this please show contact
    path('contact/', views.about_us_view, name='contact'),
    path('about-us/', views.about_us_view, name='about_us'),
    path('privacy-policy/', views.privacy_policy_view, name='privacy_policy'),
    path('terms-of-service/', views.terms_of_service_view, name='terms_of_service'),

    # path('home/', views.api_view, name='index'),
    # path('bootstrap', views.bootstrap, name='bootstrap'),
    # # Blog Site
    # path('blogs', views.blog, name='blogs'),
    # path('blog', PostListView.as_view(), name='post-list'),
    # path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    # path('categories/', CategoryListView.as_view(), name='category-list'),
    # path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),

    path('pricing/', views.pricing_section_list, name='pricing-list'),
    path('pricing/plan/<slug:slug>/', views.pricing_plan_detail, name='pricing-plan-detail'),
    path('pricing/<slug:slug>/comparison/', views.pricing_comparison, name='pricing-comparison'),
    path('pricing/<slug:slug>/', views.pricing_section_detail, name='pricing-detail'),

]



