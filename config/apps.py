
import os
from .settings import BASE_DIR

APPLICATION_BATH = [
    # os.path.join(BASE_DIR, 'apps', 'carrental'),
    # os.path.join(BASE_DIR, 'apps', 'home'),
    # os.path.join(BASE_DIR, 'apps', 'authentication'),
    # os.path.join(BASE_DIR, 'apps', 'ecommerce'),
]


# Number of minutes of inactivity before a user is marked offline
USER_ONLINE_TIMEOUT = 10

# Number of seconds that we will keep track of inactive users for before 
# their last seen is removed from the cache
USER_LASTSEEN_TIMEOUT = 60 * 60 * 24 * 7


INSTALLED_HOME_APPS = [
    # 'homepage.apps.HomepageConfig',
    # # 'accounts.apps.AccountsConfig',
    # 'users.apps.UsersConfig',
    # 'product.apps.ProductConfig',
    # # 'ratemanagement.apps.RatemanagementConfig',
    # # 'vehicle.apps.VehicleConfig',

    # 'rest_framework',
    # 'corsheaders',
    # 'mptt',
    # 'stripe',
    # 'whitenoise.runserver_nostatic',
]

STRIPE_PUBLIC_KEY = 'pk_test_51NwknCERtV8peHZwymDvL01nqL6vXAs46EdmkD7WkiCukQ0VoZWwAKlmnm12gzU4Qleb3yNW8SfOiOyWm8EaWtKt00Ryx2eXvr'
STRIPE_SECRET_KEY = 'your_stripe_secret_key'

if True:
    INSTALLED_HOME_APPS += [
        'debug_toolbar',
        # 'debug_panel',
    ]



from django.urls import path, include

apps_urls = [
    'homepage.urls',
    'product.urls',
    'users.urls'
    # 'accounts.urls'
    # "ratemanagement.urls",
    # 'vehicle.urls',

]

AUTH_USER_MODEL = 'users.CustomUser'

APPS_MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'core.middleware.ActiveUserMiddleware'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',

    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],

    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
    ],

    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DATE_INPUT_FORMATS': ['%Y-%m-%d', '%d/%m/%Y'],
    'TIME_INPUT_FORMATS': ['%H:%M:%S', '%I:%M %p'], 
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,  # Set the number of items per page
}


# Haystack Settings
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack_indexes',
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'



# Cache settings 
CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 3600   # this number equal 1h
CACHE_MIDDLEWARE_KEY_PREFIX = ''


LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'),)

from django.utils.translation import gettext_lazy as _
LANGUAGES = [
    ('ar', _('Arabic')),
    ('en', _('English')),
]


CORS_ALLOWED_ORIGINS = [
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:4200",  # Add your frontend origin(s) here
]