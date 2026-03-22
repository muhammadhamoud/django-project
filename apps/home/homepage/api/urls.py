from django.urls import path, include
from . import views
# from .views import PostListView, PostDetailView, CategoryListView, CategoryDetailView
app_name = 'homepage'

urlpatterns = [
    # path('site-information/', views.site_information, name='site-information-list'),
    path('site-all/', views.CombinedSiteDataView.as_view(), name='site-list'),
    path('site-information/', views.SiteInformationListView.as_view(), name='site-information-list'),
    path('site-metadata/', views.SiteMetaDataListView.as_view(), name='site-metadata-list'),
    path('site-additional/', views.SiteInformationAdditionalListView.as_view(), name='site-additional-list'),
    path('model/<str:model_name>/', views.CustomModelDataView.as_view(), name='get_data_for_model'),
    path('all-model-data/', views.AllModelDataView.as_view(), name='all_model_data'),
]

urlpatterns += [

    # path('site/', views.SiteInformationAPIView.as_view(), name='index'),
    # path('site/', views.site_information, name='site_information'),
    
    # Define URL pattern for the get_data_for_model view

    # path('', views.index, name='index'),

    # path('bootstrap', views.bootstrap, name='bootstrap'),
    # # Blog Site
    # path('blogs', views.blog, name='blogs'),
    # path('blog', PostListView.as_view(), name='post-list'),
    # path('post/<slug:slug>/', PostDetailView.as_view(), name='post-detail'),
    # path('categories/', CategoryListView.as_view(), name='category-list'),
    # path('category/<slug:slug>/', CategoryDetailView.as_view(), name='category-detail'),

]
