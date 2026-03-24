import os
from .settings import BASE_DIR
from decouple import config
from datetime import date
from django.utils.translation import gettext_lazy as _
CART_SESSION_ID = 'cart'
END_DATE = date(2025,12,31)
EXTENDED_DEBUG = config('DEBUG', cast=bool)

# TODO Change this on productions
DOMAIN = 'localhost:4200'

HOSTING = ['localhost', '127.0.0.1', 'localhost:4200']
LOCALHOSTING = ['http://localhost:4200', ]

if EXTENDED_DEBUG:
    EXTENDED_ALLOWED_HOSTS = HOSTING
    CORS_ORIGIN_WHITELIST= LOCALHOSTING
    CORS_ALLOWED_ORIGINS = LOCALHOSTING
else:
    EXTENDED_ALLOWED_HOSTS = [f'{DOMAIN}', f'www.{DOMAIN}', f'api.{DOMAIN}', f'www.api.{DOMAIN}'] + HOSTING
    CORS_ORIGIN_WHITELIST= [f'{DOMAIN}', f'www.{DOMAIN}', f'api.{DOMAIN}', f'www.api.{DOMAIN}'] + HOSTING
    CORS_ALLOWED_ORIGINS = [f'https://{DOMAIN}', f'https://www.{DOMAIN}', f'https://api.{DOMAIN}', f'https://www.api.{DOMAIN}'] + LOCALHOSTING

APPLICATION_BATH = [
    os.path.join(BASE_DIR, 'apps', 'accounts'),
    os.path.join(BASE_DIR, 'apps', 'properties'),
    os.path.join(BASE_DIR, 'apps', 'settings'),
    os.path.join(BASE_DIR, 'apps', 'reports'),
    os.path.join(BASE_DIR, 'apps', 'dashboard'),
    os.path.join(BASE_DIR, 'apps', 'data'),
    os.path.join(BASE_DIR, 'apps', 'home'),
    os.path.join(BASE_DIR, 'apps', 'core'),
    # os.path.join(BASE_DIR, 'apps', 'ecommerce'),
    # os.path.join(BASE_DIR, 'apps', 'address'),
    # os.path.join(BASE_DIR, 'apps', 'shop'),
    # os.path.join(BASE_DIR, 'apps', 'cuttern'),
    # os.path.join(BASE_DIR, 'apps', 'realestate'),
    # os.path.join(BASE_DIR, 'apps', 'blogs'),
]

NEW_APPS = [
    'accounts',
    'properties',
    'reports',
    'dashboard',
    'data',
    'settings',

    # 'mappings',
    # 'segments',
    # 'mappers',
    # Mappings
    # Home
    'homepage',
    # 'communication',
    # 'blogs',
    'core',
    # 'address',
    # 'addresses',
    
    # # ecommerce
    # 'categories',
    # 'products',
    # 'prices',
    # 'coupons',
    # 'carts',
    # 'orders',
    # 'payment',


    # # cuttern
    # 'cars',
    
    
    
    # 'warehouse',
    # 'plotter',

    # 'shop',
    # 'orders',
    # 'payment',
    # 'coupons',
    # 'cart',
        
    # 'address',
    # 'googlemap',
    # 'plotter_payment',
    # 'cart',
    # 'contents',
    # 'store',
    # 'user_profile',
    # 'order',
    # 'shopingcart',
    # 'sample',
]

INTERNAL_APPS = []
for APP in NEW_APPS:
    INTERNAL_APPS.append(F'{APP}.apps.{APP.title()}Config')

EXTERNAL_APPS = [
    'rest_framework',
    'tailwind',
    'themes',
    'parler',
    # 'mptt',
    # 'stripe',
    # 'django_celery_results',
    # 'django_countries',
    # 'djmoney',
    # 'cities',
    # conda install -c conda-forge gdal
    # 'djmoney.contrib.exchange',
    # 'rosetta',
    # 'localflavor',
]

TAILWIND_APP_NAME = 'themes'

CURRENCIES = ('USD', 'AED', 'EUR')
# EXCHANGE_BACKEND = 'djmoney.contrib.exchange.backends.FixerBackend'

APPS_EXTENDED = EXTERNAL_APPS + INTERNAL_APPS

APPS_URLS = []
for APP in NEW_APPS:
    APPS_URLS.append(f'{APP}.urls')

APPS_MIDDLEWARE = [
    # 'corsheaders.middleware.CorsMiddleware',
    # 'core.middleware.ActiveUserMiddleware'
]

if EXTENDED_DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    
    # Extra places for collectstatic to find static files.
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
        os.path.join(BASE_DIR, 'apps', 'static'),
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles') #config('STATIC_ROOT')
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'static'),
        # os.path.join(BASE_DIR, 'apps', 'static'),
    ]

    # STATICFILES_DIRS = [BASE_DIR / "staticfiles",]
    # print(STATIC_ROOT)
    # STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    # # Extra places for collectstatic to find static files.
    # STATICFILES_DIRS = [
    #     os.path.join(BASE_DIR, 'static'),
    # ]

# STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

FIXTURE_DIRS = [
    os.path.join(BASE_DIR, 'fixtures'),  
]

# COUNTRIES_FLAG_URL =  '/assets/flags'


AUTH_USER_MODEL = 'accounts.CustomUser'

# Number of minutes of inactivity before a user is marked offline
USER_ONLINE_TIMEOUT = 10

# Number of seconds that we will keep track of inactive users for before 
# their last seen is removed from the cache
USER_LASTSEEN_TIMEOUT = 60 * 60 * 24 * 7


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    
    'DEFAULT_PERMISSION_CLASSES': [
        # 'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
        # 'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',
        # 'rest_framework.permissions.IsAuthenticatedOrReadOnly',

    ],

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
    ],

    # 'DEFAULT_THROTTLE_CLASSES': [
    #     'rest_framework.throttling.UserRateThrottle',
    # ],

    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DATE_INPUT_FORMATS': ['%Y-%m-%d', '%d/%m/%Y'],
    'TIME_INPUT_FORMATS': ['%H:%M:%S', '%I:%M %p'], 
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,  # Set the number of items per page
}


# Config simple jwt as default authentication and pagination
REST_FRAMEWORK.update({
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 12,
    
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
})

# Setup JWT expired date
import datetime
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=14),
}

# CORS
# CORS_ORIGIN_ALLOW_ALL = True  # If this is used then `CORS_ORIGIN_WHITELIST` will not have any effect
# CORS_ALLOW_ALL_ORIGINS = True  # Allow all origins for development (you can change this in production)

CORS_ALLOW_CREDENTIALS = True
# CORS_ALLOW_HEADERS = "access-control-allow-origin"
# CORS_ALLOW_METHODS = ['GET', 'OPTIONS']  # Allow GET and OPTIONS methods

# For production, you should specify allowed origins explicitly:
CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]
CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

# CORS_ALLOW_HEADERS = [
#     'content-type', 
#     "access-control-allow-origin",
#     'authorization', 
#     'accept',
#     'accept-encoding',
#     'content-type',
#     'dnt',
#     'origin',
#     'user-agent',
#     'x-csrftoken',
#     'x-requested-with',
# ]

# CSRF_COOKIE_SECURE = True
# SESSION_COOKIE_SECURE = True

SITE_ID = 1

if EXTENDED_DEBUG:
    APPS_EXTENDED += [
        'debug_toolbar',
        # 'debug_panel',
    ]

if EXTENDED_DEBUG:
    APPS_MIDDLEWARE +=[
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]

# CART_SESSION_ID = 'cart'

WEBISTE_NAME=DOMAIN

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
SECRET_KEY_CONFIG = config('SECRET_KEY')
# WEBISTE_NAME = config('WEBISTE_NAME')
# EMAIL_HOST = config('EMAIL_HOST')
# EMAIL_PORT = config('EMAIL_PORT', cast=int)
# EMAIL_USE_SSL = config('EMAIL_USE_SSL', cast=bool)
# EMAIL_HOST_USER = config('EMAIL_HOST_USER')
# DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL')

EMAIL_DOMAIN = 'roinsight.com'
EMAIL_HOST=f'mail.{EMAIL_DOMAIN}'
EMAIL_PORT=465
EMAIL_USE_SSL=True
EMAIL_HOST_USER=f'support@{EMAIL_DOMAIN}'
DEFAULT_FROM_EMAIL=f'support@{EMAIL_DOMAIN}'
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

# Stripe settings
STRIPE_PUBLISHABLE_KEY = config('STRIPE_PUBLISHABLE_KEY') 
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY')
STRIPE_API_VERSION=''
STRIPE_WEBHOOK_SECRET=config('STRIPE_WEBHOOK_SECRET')
PAYMENT_SUCCESS_URL=f'https://{DOMAIN}/products/orders/success'
PAYMENT_CANCEL_URL=f'https://{DOMAIN}/products/orders/cancel'
APPEND_SLASH=False

# Redis settings
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 1

# # Google Map settings
# GOOGLE_MAPS_API_WEB_KEY = config('GOOGLE_MAPS_API_WEB_KEY')
# GOOGLE_MAPS_API_SERVER_KEY = config('GOOGLE_MAPS_API_SERVER_KEY')

# CITIES_DATA_DIR = '/cities/'

# CITIES_FILES = {
#     # ...
#     'city': {
#        'filename': 'cities1000.zip',
#        'urls':     ['http://download.geonames.org/export/dump/'+'{filename}']
#     },
#     # ...
# }

# CITIES_CONTINENT_DATA = {
#     'AF': ('Africa', 6255146),
#     'AS': ('Asia', 6255147),
#     'EU': ('Europe', 6255148),
#     'NA': ('North America', 6255149),
#     'OC': ('Oceania', 6255151),
#     'SA': ('South America', 6255150),
#     'AN': ('Antarctica', 6255152),
# }

# CITIES_AIRPORT_TYPES = (
#     ('iata', _("IATA (Airport) Code")),
#     ('icao', _("ICAO (Airport) Code")),
#     ('faac', _("FAAC (Airport) Code")),
# )

# CITIES_ALTERNATIVE_NAME_TYPES = (
#     ('name', _("Name")),
#     ('abbr', _("Abbreviation")),
#     ('link', _("Link")),
# )

# # Assuming GDAL is installed in a standard system path (adjust as needed)
# import sys
# # import gdal
# # print(gdal.__version__)
# # GDAL_LIBRARY_PATH = os.path.join(sys.exec_prefix, 'lib', 'gdal')
# GDAL_LIBRARY_PATH = fr"C:\Users\maalh836\Downloads\gdal-3.8.5.tar\gdal-3.8.5"


# Celery Configuration Options
CELERY_TIMEZONE = "Australia/Tasmania"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60
# CELERY_RESULT_BACKEND = 'django-db'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_CACHE_BACKEND = 'django-cache'
CELERY_BROKER_URL = "redis://localhost:6379"

# celery setting.
CELERY_CACHE_BACKEND = 'default'

# # django setting.
# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
#         'LOCATION': 'my_cache_table',
#     }
# }


SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 7 days in seconds
SESSION_EXPIRE_AT_BROWSER_CLOSE = False