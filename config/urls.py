"""
URL configuration for config project.
"""
from django.contrib import admin
from django.urls import include, path, re_path
from django.conf import settings
from django.conf.urls.static import static
from .apps import apps_urls
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _
from django.views.static import serve
from .workspace import DOMAIN

from django.http import HttpResponseRedirect

def api_view(request):
    # Redirect to the specific site
    return HttpResponseRedirect(f'https://{DOMAIN}/')

urlpatterns = [
    # path('', api_view, name='index'),
    path("admin/", admin.site.urls),
    # ✅ Accounts app (HTML views)
    # path("accounts/", include("accounts.urls")),
    # re_path(r'^assets/(?P<path>.*)$', TemplateView.as_view(template_name='index.html')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
] 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# urlpatterns = i18n_patterns(
#     path('admin/', admin.site.urls),
#     path('rosetta/', include('rosetta.urls')),
#     # path('', include('shop.urls', namespace='shop')),
# )

# from .workspace import APPS_URLS
# from django.urls import include

# for url in APPS_URLS:
#     urlpatterns.append(path('api/', include(url)),)

from django.urls import path, include
APPS_URLPATTERNS, APIS_URLSPATTERNS = [], []
from .workspace import NEW_APPS
# Generate Automatic URLS
for APP in NEW_APPS:

    if APP in ['homepage', 'communication']:
        urlpatterns += i18n_patterns(
        path('', include(f"{APP}.urls")),
        )
        # urlpatterns += [path('api/', include(f"{APP}.api.urls"))]
    else:
        urlpatterns.append(
            path('', include(f"{APP}.urls"))
        )
        urlpatterns.append(
            path('api/', include(f"{APP}.api.urls"))
        )

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    # urlpatterns += [
    #     path('rosetta/', include('rosetta.urls')),
    # ]