import os
from pathlib import Path
from datetime import timedelta
from decouple import config, Csv
import dj_database_url
from django.urls import reverse_lazy

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Security Settings
SECRET_KEY = config('SECRET_KEY', default='django-insecure-tiipe-novatrix-production-master-secret-key-2026')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=Csv())

# ==============================================================================
# MULTI-TENANCY APPLICATION CONFIGURATION (django-tenants)
# ==============================================================================

SHARED_APPS = [
    'django_tenants',  # Must be first
    'apps.core',       # Contains ClientTenant and Domain models
    'unfold',          # Modern Tailwind CSS Django Admin theme (must precede django.contrib.admin)
    'unfold.contrib.filters',
    'unfold.contrib.forms',
    'unfold.contrib.inlines',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party shared libraries
    'rest_framework',
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    'corsheaders',
    'drf_spectacular',
    'django_filters',
    
    # Shared User & Identity Application
    'apps.users',
]

TENANT_APPS = [
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.messages',
    'rest_framework',
    
    # Tenant Isolated Business Applications
    'apps.cms',
    'apps.tiipe_lms',
    'apps.novatrix_services',
    'apps.payments',
    'apps.notifications',
    'apps.files',
]

INSTALLED_APPS = list(SHARED_APPS) + [app for app in TENANT_APPS if app not in SHARED_APPS]

TENANT_MODEL = "core.ClientTenant"
TENANT_DOMAIN_MODEL = "core.Domain"

PUBLIC_SCHEMA_URLCONF = 'config.urls_public'
ROOT_URLCONF = 'config.urls_tenants'

# Database Multi-Tenant Router
DATABASE_ROUTERS = (
    'django_tenants.routers.TenantSyncRouter',
)

# Custom User Model
AUTH_USER_MODEL = 'users.CustomUser'

# ==============================================================================
# MIDDLEWARE CONFIGURATION
# ==============================================================================

MIDDLEWARE = [
    'apps.core.middleware.TenantHeaderAndHostMiddleware',  # Custom tenant detector (header + host)
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==============================================================================
# DATABASE CONFIGURATION (PostgreSQL Multi-Schema)
# ==============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': config('DB_NAME', default='tiipe_novatrix_db'),
        'USER': config('DB_USER', default='postgres'),
        'PASSWORD': config('DB_PASSWORD', default='postgres'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='5432'),
    }
}

# Support for DATABASE_URL if present
DATABASE_URL = config('DATABASE_URL', default=None)
if DATABASE_URL:
    db_config = dj_database_url.parse(DATABASE_URL)
    db_config['ENGINE'] = 'django_tenants.postgresql_backend'
    DATABASES['default'] = db_config

# Password Validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 8}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ==============================================================================
# TEMPLATES & STATIC FILES
# ==============================================================================

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ==============================================================================
# AWS S3 / DIGITALOCEAN SPACES FILE STORAGE CONFIGURATION
# ==============================================================================

USE_S3 = config('USE_S3', default=False, cast=bool)

if USE_S3:
    AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME')
    AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
    AWS_S3_ENDPOINT_URL = config('AWS_S3_ENDPOINT_URL', default=None)
    AWS_S3_CUSTOM_DOMAIN = config('AWS_S3_CUSTOM_DOMAIN', default=None)
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    AWS_DEFAULT_ACL = 'public-read'
    
    DEFAULT_FILE_STORAGE = 'apps.files.storage.TenantMediaStorage'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/' if AWS_S3_CUSTOM_DOMAIN else f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/'
else:
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# ==============================================================================
# REST FRAMEWORK & SIMPLE JWT CONFIGURATION
# ==============================================================================

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_PAGINATION_CLASS': 'apps.core.pagination.StandardResultsSetPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'apps.core.exceptions.custom_exception_handler',
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=config('JWT_ACCESS_TOKEN_LIFETIME_MINUTES', default=60, cast=int)),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=config('JWT_REFRESH_TOKEN_LIFETIME_DAYS', default=14, cast=int)),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': config('JWT_SIGNING_KEY', default=SECRET_KEY),
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# ==============================================================================
# DRF SPECTACULAR (SWAGGER / OPENAPI 3.0)
# ==============================================================================

SPECTACULAR_SETTINGS = {
    'TITLE': 'TIIPE & Novatrix Unified Multi-Tenant API',
    'DESCRIPTION': (
        'Production REST API backend serving The Impact Institute for Public Education (TIIPE - Parent) '
        'and Novatrix (Subsidiary) across Web, iOS, and Android applications.'
    ),
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': r'/api/v[0-9]',
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': True,
    },
}

# ==============================================================================
# UNFOLD MODERN TAILWIND CSS ADMIN THEME CONFIGURATION
# ==============================================================================

UNFOLD = {
    "SITE_TITLE": "TIIPE & Novatrix Master Admin",
    "SITE_HEADER": "TIIPE / Novatrix",
    "SITE_SUBHEADER": "Enterprise Multi-Tenant Control Hub",
    "SITE_URL": "/",
    "SITE_SYMBOL": "account_balance",
    "DASHBOARD_CALLBACK": "apps.core.dashboard.dashboard_callback",
    "THEME": "dark",
    "COLORS": {
        "primary": {
            "50": "239 246 255",
            "100": "219 234 254",
            "200": "191 219 254",
            "300": "147 197 253",
            "400": "96 165 250",
            "500": "59 130 246",
            "600": "37 99 235",
            "700": "30 58 138",
            "800": "30 41 59",
            "900": "15 23 42",
            "950": "2 6 23",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": "Master Overview",
                "separator": True,
                "items": [
                    {
                        "title": "Master Dashboard",
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                    {
                        "title": "Public Gateway",
                        "icon": "language",
                        "link": "/",
                    },
                    {
                        "title": "Swagger UI Docs",
                        "icon": "code",
                        "link": "/api/docs/",
                    },
                    {
                        "title": "Health Telemetry",
                        "icon": "monitor_heart",
                        "link": "/health/",
                    },
                ],
            },
            {
                "title": "Multi-Tenant & Identity (Shared)",
                "separator": True,
                "items": [
                    {
                        "title": "Tenant Schemas",
                        "icon": "domain",
                        "link": reverse_lazy("admin:core_clienttenant_changelist"),
                    },
                    {
                        "title": "Domain Routes",
                        "icon": "dns",
                        "link": reverse_lazy("admin:core_domain_changelist"),
                    },
                    {
                        "title": "User Accounts",
                        "icon": "people",
                        "link": reverse_lazy("admin:users_customuser_changelist"),
                    },
                    {
                        "title": "User Profiles",
                        "icon": "badge",
                        "link": reverse_lazy("admin:users_userprofile_changelist"),
                    },
                    {
                        "title": "Tenant Memberships",
                        "icon": "group_work",
                        "link": reverse_lazy("admin:users_tenantmembership_changelist"),
                    },
                ],
            },
            {
                "title": "TIIPE — Education & Health (Parent)",
                "separator": True,
                "items": [
                    {
                        "title": "Educational Programs",
                        "icon": "school",
                        "link": reverse_lazy("admin:tiipe_lms_program_changelist"),
                    },
                    {
                        "title": "Mentor Applications",
                        "icon": "how_to_reg",
                        "link": reverse_lazy("admin:tiipe_lms_mentorapplication_changelist"),
                    },
                    {
                        "title": "Mentor Availability",
                        "icon": "event_available",
                        "link": reverse_lazy("admin:tiipe_lms_mentoravailability_changelist"),
                    },
                    {
                        "title": "Mentorship Sessions",
                        "icon": "calendar_month",
                        "link": reverse_lazy("admin:tiipe_lms_mentorshipsession_changelist"),
                    },
                    {
                        "title": "Learning Modules",
                        "icon": "menu_book",
                        "link": reverse_lazy("admin:tiipe_lms_learningmodule_changelist"),
                    },
                    {
                        "title": "Public Health Resources",
                        "icon": "health_and_safety",
                        "link": reverse_lazy("admin:tiipe_lms_publichealthresource_changelist"),
                    },
                    {
                        "title": "Policy & Research Briefs",
                        "icon": "description",
                        "link": reverse_lazy("admin:tiipe_lms_policybrief_changelist"),
                    },
                    {
                        "title": "Governance Documents",
                        "icon": "policy",
                        "link": reverse_lazy("admin:cms_governancedocument_changelist"),
                    },
                    {
                        "title": "Board of Directors",
                        "icon": "groups",
                        "link": reverse_lazy("admin:cms_boardmember_changelist"),
                    },
                    {
                        "title": "AdieTalk Radio & Media",
                        "icon": "radio",
                        "link": reverse_lazy("admin:cms_mediabroadcast_changelist"),
                    },
                    {
                        "title": "Webinars",
                        "icon": "video_camera_front",
                        "link": reverse_lazy("admin:cms_webinar_changelist"),
                    },
                ],
            },
            {
                "title": "Novatrix — Tech & Solutions (Subsidiary)",
                "separator": True,
                "items": [
                    {
                        "title": "4 Service Pillars",
                        "icon": "category",
                        "link": reverse_lazy("admin:novatrix_services_servicepillar_changelist"),
                    },
                    {
                        "title": "Industry Solutions",
                        "icon": "corporate_fare",
                        "link": reverse_lazy("admin:novatrix_services_industrysolution_changelist"),
                    },
                    {
                        "title": "Projects & Case Studies",
                        "icon": "business_center",
                        "link": reverse_lazy("admin:novatrix_services_projectcasestudy_changelist"),
                    },
                    {
                        "title": "Technology Courses",
                        "icon": "terminal",
                        "link": reverse_lazy("admin:novatrix_services_trainingcourse_changelist"),
                    },
                    {
                        "title": "Training Cohorts",
                        "icon": "schedule",
                        "link": reverse_lazy("admin:novatrix_services_trainingcohort_changelist"),
                    },
                    {
                        "title": "Project Inquiries",
                        "icon": "forum",
                        "link": reverse_lazy("admin:novatrix_services_projectinquiry_changelist"),
                    },
                    {
                        "title": "Training Inquiries",
                        "icon": "record_voice_over",
                        "link": reverse_lazy("admin:novatrix_services_traininginquiry_changelist"),
                    },
                    {
                        "title": "Client Support Tickets",
                        "icon": "support_agent",
                        "link": reverse_lazy("admin:novatrix_services_supportticket_changelist"),
                    },
                ],
            },
            {
                "title": "Finance & Communications",
                "separator": True,
                "items": [
                    {
                        "title": "501(c)(3) Donations",
                        "icon": "volunteer_activism",
                        "link": reverse_lazy("admin:payments_donation_changelist"),
                    },
                    {
                        "title": "Payment Transactions",
                        "icon": "receipt_long",
                        "link": reverse_lazy("admin:payments_paymenttransaction_changelist"),
                    },
                    {
                        "title": "Invoices",
                        "icon": "request_quote",
                        "link": reverse_lazy("admin:payments_invoice_changelist"),
                    },
                    {
                        "title": "Gateway Webhooks",
                        "icon": "webhook",
                        "link": reverse_lazy("admin:payments_webhooklog_changelist"),
                    },
                    {
                        "title": "Hero Banners",
                        "icon": "view_carousel",
                        "link": reverse_lazy("admin:cms_herosection_changelist"),
                    },
                    {
                        "title": "Impact Counters",
                        "icon": "trending_up",
                        "link": reverse_lazy("admin:cms_impactmetric_changelist"),
                    },
                    {
                        "title": "Articles & News",
                        "icon": "newspaper",
                        "link": reverse_lazy("admin:cms_article_changelist"),
                    },
                    {
                        "title": "Contact Inquiries",
                        "icon": "mail",
                        "link": reverse_lazy("admin:cms_contactmessage_changelist"),
                    },
                    {
                        "title": "Push Device Tokens",
                        "icon": "devices",
                        "link": reverse_lazy("admin:notifications_pushdevicetoken_changelist"),
                    },
                    {
                        "title": "Notification Logs",
                        "icon": "notifications_active",
                        "link": reverse_lazy("admin:notifications_notificationlog_changelist"),
                    },
                    {
                        "title": "Media Assets",
                        "icon": "perm_media",
                        "link": reverse_lazy("admin:files_mediaasset_changelist"),
                    },
                    {
                        "title": "Document Uploads",
                        "icon": "folder",
                        "link": reverse_lazy("admin:files_documentupload_changelist"),
                    },
                ],
            },
        ],
    },
}

# ==============================================================================
# CORS HEADERS CONFIGURATION
# ==============================================================================

CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,http://localhost:5173,http://localhost:5174,http://localhost:5175,http://localhost:4173,http://localhost:8080,https://impactinstituteglobal.org,https://www.impactinstituteglobal.org,https://thenovatrix.com,https://www.thenovatrix.com',
    cast=Csv()
)
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-tenant',  # Custom mobile and web tenant header
]

# ==============================================================================
# CELERY & REDIS CACHING
# ==============================================================================

REDIS_URL = config('REDIS_URL', default='redis://localhost:6379/0')
CELERY_BROKER_URL = config('CELERY_BROKER_URL', default='redis://localhost:6379/1')
CELERY_RESULT_BACKEND = config('CELERY_RESULT_BACKEND', default='redis://localhost:6379/1')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# ==============================================================================
# EMAIL SERVICE & GATEWAY KEYS
# ==============================================================================

EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.console.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='smtp.sendgrid.net')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='notifications@impactinstituteglobal.org')
TIIPE_FROM_EMAIL = config('TIIPE_FROM_EMAIL', default='info@impactinstituteglobal.org')
NOVATRIX_FROM_EMAIL = config('NOVATRIX_FROM_EMAIL', default='contact@thenovatrix.com')

# Third-Party Gateway API Keys
STRIPE_PUBLIC_KEY = config('STRIPE_PUBLIC_KEY', default='')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='')
STRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET', default='')
PAYSTACK_PUBLIC_KEY = config('PAYSTACK_PUBLIC_KEY', default='')
PAYSTACK_SECRET_KEY = config('PAYSTACK_SECRET_KEY', default='')

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
