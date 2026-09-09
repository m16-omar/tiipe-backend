import os
from pathlib import Path
from datetime import timedelta
from decouple import config, Csv
import dj_database_url

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
    'jazzmin',         # Modern Django Admin theme (must precede django.contrib.admin)
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
# JAZZMIN MODERN ADMIN THEME CONFIGURATION
# ==============================================================================

JAZZMIN_SETTINGS = {
    "site_title": "TIIPE & Novatrix Master Admin",
    "site_header": "TIIPE / Novatrix Admin",
    "site_brand": "TIIPE & Novatrix",
    "welcome_sign": "Unified Multi-Tenant Management Portal",
    "copyright": "TIIPE & Novatrix Unified Master Systems",
    "search_model": ["users.CustomUser", "core.ClientTenant", "tiipe_lms.Program", "novatrix_services.ServicePillar"],
    "user_avatar": None,
    "topmenu_links": [
        {"name": "Master Dashboard", "url": "/", "permissions": ["auth.view_user"]},
        {"name": "Swagger UI", "url": "/api/docs/", "new_window": True},
        {"name": "ReDoc", "url": "/api/redoc/", "new_window": True},
        {"name": "Health Telemetry", "url": "/health/", "new_window": True},
    ],
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": [
        "core",
        "users",
        "tiipe_lms",
        "novatrix_services",
        "cms",
        "payments",
        "notifications",
        "files",
        "auth",
    ],
    "custom_links": {
        "core": [{
            "name": "Live API Swagger UI",
            "url": "/api/docs/",
            "icon": "fas fa-code",
            "permissions": ["core.view_clienttenant"]
        }, {
            "name": "Live ReDoc Specs",
            "url": "/api/redoc/",
            "icon": "fas fa-book",
            "permissions": ["core.view_clienttenant"]
        }, {
            "name": "Public Master Gateway",
            "url": "/",
            "icon": "fas fa-network-wired",
            "permissions": ["core.view_clienttenant"]
        }]
    },
    "custom_css": "css/custom_admin.css",
    "custom_js": "js/custom_admin.js",
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.Group": "fas fa-user-friends",
        "users.CustomUser": "fas fa-user-shield",
        "users.UserProfile": "fas fa-id-badge",
        "users.TenantMembership": "fas fa-user-tag",
        "core.ClientTenant": "fas fa-building",
        "core.Domain": "fas fa-globe",
        "cms.HeroSection": "fas fa-tv",
        "cms.NavigationMenu": "fas fa-bars",
        "cms.GovernanceDocument": "fas fa-file-contract",
        "cms.BoardMember": "fas fa-user-tie",
        "cms.MediaBroadcast": "fas fa-podcast",
        "cms.Webinar": "fas fa-video",
        "cms.ImpactMetric": "fas fa-chart-line",
        "cms.PublicBenefitStatement": "fas fa-award",
        "cms.ArticleCategory": "fas fa-tags",
        "cms.Article": "fas fa-newspaper",
        "cms.FAQ": "fas fa-question-circle",
        "cms.Testimonial": "fas fa-comment-dots",
        "cms.ContactMessage": "fas fa-envelope-open-text",
        "cms.EventNotice": "fas fa-calendar-alt",
        "tiipe_lms.Program": "fas fa-graduation-cap",
        "tiipe_lms.MentorApplication": "fas fa-user-graduate",
        "tiipe_lms.MentorAvailability": "fas fa-clock",
        "tiipe_lms.MentorshipSession": "fas fa-chalkboard-teacher",
        "tiipe_lms.LearningModule": "fas fa-book-reader",
        "tiipe_lms.Lesson": "fas fa-list-ol",
        "tiipe_lms.LearnerProgress": "fas fa-tasks",
        "tiipe_lms.PublicHealthResource": "fas fa-heartbeat",
        "tiipe_lms.PolicyBrief": "fas fa-file-alt",
        "novatrix_services.ServicePillar": "fas fa-cubes",
        "novatrix_services.IndustrySolution": "fas fa-industry",
        "novatrix_services.ProjectCaseStudy": "fas fa-briefcase",
        "novatrix_services.TrainingCourse": "fas fa-laptop-code",
        "novatrix_services.TrainingCohort": "fas fa-users-class",
        "novatrix_services.ProjectInquiry": "fas fa-comments",
        "novatrix_services.TrainingInquiry": "fas fa-user-check",
        "novatrix_services.SupportTicket": "fas fa-headset",
        "novatrix_services.CapabilityDownload": "fas fa-cloud-download-alt",
        "payments.Donation": "fas fa-hand-holding-usd",
        "payments.DonationAllocation": "fas fa-donate",
        "payments.PaymentTransaction": "fas fa-receipt",
        "payments.Invoice": "fas fa-file-invoice-dollar",
        "payments.WebhookLog": "fas fa-exchange-alt",
        "notifications.PushDeviceToken": "fas fa-mobile-alt",
        "notifications.NotificationLog": "fas fa-bell",
        "notifications.EmailTemplate": "fas fa-mail-bulk",
        "files.MediaAsset": "fas fa-photo-video",
        "files.DocumentUpload": "fas fa-folder-open",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "changeform_format": "horizontal_tabs",
    "related_modal_active": True,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-primary",
    "navbar": "navbar-dark navbar-navy",
    "no_navbar_border": False,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "darkly",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    }
}

# ==============================================================================
# CORS HEADERS CONFIGURATION
# ==============================================================================

CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=False, cast=bool)
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,http://localhost:5173,http://localhost:8080,https://impactinstituteglobal.org,https://www.impactinstituteglobal.org,https://thenovatrix.com,https://www.thenovatrix.com',
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
