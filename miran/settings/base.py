from datetime import timedelta
from os.path import join, normpath
from pathlib import Path

from django.urls import reverse_lazy

from decouple import config


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default=False, cast=str)
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default=False, cast=bool)

ALLOWED_HOSTS = ["*"]

AUTH_USER_MODEL = "users.User"
AUTHENTICATION_BACKENDS = ["django.contrib.auth.backends.ModelBackend"]
# Application definition
DJANGO_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.import_export",
    "modeltranslation",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.contrib.postgres",
]
THIRD_PARTY_APPS = [
    "rest_framework",
    "corsheaders",
    "import_export",
    "django_filters",
    "drf_spectacular",
    "silk",
]
# local apps
LOCAL_APPS = [
    "miran.users",
    "miran.products",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
SITE_ID = 1


MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "silk.middleware.SilkyMiddleware",
]

ROOT_URLCONF = "miran.urls"


TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]


WSGI_APPLICATION = "miran.wsgi.application"
# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("POSTGRES_DB", cast=str),
        "USER": config("POSTGRES_USER", cast=str),
        "PASSWORD": config("POSTGRES_PASSWORD", cast=str),
        "HOST": config("POSTGRES_HOST", cast=str),
        "PORT": config("POSTGRES_PORT", cast=str),
        "ATOMIC_REQUESTS": True,
    }
}
# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/
LANGUAGE_CODE = "en"

TIME_ZONE = "Africa/Cairo"

USE_I18N = True

USE_L10N = True

USE_TZ = True
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = "static/"
# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

gettext = lambda s: s  # noqa
LANGUAGES = (("en", gettext("English")), ("ar", gettext("Arabic")))
MODELTRANSLATION_DEFAULT_LANGUAGE = "en"

LOCALE_PATHS = (normpath(join(BASE_DIR, "locale")),)


STATIC_DIRECTORY = "/static/"
MEDIA_DIRECTORY = "/media/"

AUTH_PASSWORD_VALIDATORS = []
AWS_QUERYSTRING_AUTH = False


""" CORS ORIGIN """
# CORS Settings - More restrictive
CORS_ORIGIN_ALLOW_ALL = False  # Don't allow all origins in production
CORS_ALLOWED_ORIGINS = config(
    "CORS_ALLOWED_ORIGINS",
    default="http://localhost:3000",
    cast=lambda v: [s.strip() for s in v.split(",")],
)
CORS_ALLOW_CREDENTIALS = True
# Security Headers
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True


""" REST FRAMEWORK """
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_PAGINATION_CLASS": "miran.services.paginator.CustomPagination",
    "PAGE_SIZE": 5,
    "DEFAULT_FILTER_BACKENDS": (
        "django_filters.rest_framework.DjangoFilterBackend",
        "miran.services.filters.CustomSearchFilter",
        "miran.services.filters.CustomOrderingFilter",
    ),
    "EXCEPTION_HANDLER": "miran.services.exceptions.validation_error_handler",
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.UserRateThrottle",
        "rest_framework.throttling.AnonRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": "5/min",
        "user": "10/min",
    },
}

""" JWT Settings"""

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=10),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=30),
    "AUTH_HEADER_TYPES": ("Token",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "UPDATE_LAST_LOGIN": True,
}

"""Import Export"""
IMPORT_EXPORT_USE_TRANSACTIONS = True


""" SPECTACULAR_SETTINGS """
SPECTACULAR_SETTINGS = {
    "TITLE": "elevate_rebuild API",
    "DESCRIPTION": "elevate_rebuild Swagger Documentation",
    "VERSION": "v1",
    "SCHEMA_PATH_PREFIX": "/en/api/",
    "SCHEMA_PATH_PREFIX_TRIM": False,
    "DEFAULT_AUTO_SCHEMA_CLASS": "elevate_rebuild.swagger.CustomSwaggerAutoSchema",
    "DEFAULT_GENERATOR_CLASS": "drf_spectacular.generators.SchemaGenerator",
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "persistAuthorization": True,
        "docExpansion": "none",
        "filter": True,
        "displayOperationId": True,
        "displayRequestDuration": True,
        "theme": "dark",
    },
    "SECURITY": [
        {
            "JWT": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
            }
        }
    ],
    "SERVE_AUTHENTICATION": ["rest_framework.authentication.SessionAuthentication"],
    "SERVE_PERMISSIONS": ["rest_framework.permissions.IsAuthenticated"],
    "SERVE_INCLUDE_SCHEMA": True,
}

"""silk"""
SILKY_AUTHENTICATION = True
SILKY_META = True

"""Unfold"""

UNFOLD = {
    "SITE_TITLE": "Miran",
    "SITE_HEADER": "Miran",
    "ENVIRONMENT": "miran.settings.base.environment_callback",
    "SHOW_LANGUAGES": True,
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": True,
        "navigation": [
            {
                "title": "Navigation",
                "items": [
                    {
                        "title": "Dashboard",
                        "icon": "dashboard",
                        "link": reverse_lazy("admin:index"),
                    },
                ],
            },
            {
                "title": "Products",
                "collapsible": 0,
                "items": [
                    {
                        "title": "Brands",
                        "icon": "branding_watermark",
                        "link": reverse_lazy("admin:products_brand_changelist"),
                    },
                    {
                        "title": "Categories",
                        "icon": "category",
                        "link": reverse_lazy("admin:products_category_changelist"),
                    },
                    {
                        "title": "Products",
                        "icon": "inventory_2",
                        "link": reverse_lazy("admin:products_product_changelist"),
                    },
                ],
            },
            {
                "title": "Users & Groups",
                "collapsible": 0,
                "items": [
                    {
                        "title": "Users",
                        "icon": "person",
                        "link": reverse_lazy("admin:users_user_changelist"),
                    },
                    {
                        "title": "Groups",
                        "icon": "group",
                        "link": reverse_lazy("admin:auth_group_changelist"),
                    },
                ],
            },
        ],
    },
    "EXTENSIONS": {
        "modeltranslation": {
            "flags": {
                "en": "🇬🇧",
                "ar": "🇸🇦",
            },
        },
    },
}


def environment_callback(request):
    is_live = config("PRODUCTION", default=False, cast=bool)
    is_staging = config("STAGING", default=False, cast=bool)

    if is_live:
        return ["Production", "danger"]
    elif is_staging:
        return ["Staging", "warning"]
    else:
        return ["Local", "success"]


# Redis Settings
REDIS_HOST = config("REDIS_HOST", default="redis")
REDIS_PORT = config("REDIS_PORT", default=6379)
REDIS_DB = config("REDIS_DB", default=0)
REDIS_PASSWORD = config("REDIS_PASSWORD", default=None)
# Cache settings
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            # "PASSWORD": REDIS_PASSWORD,
        },
    }
}
# RQ Configuration
RQ_QUEUES = {
    "default": {
        "HOST": config("REDIS_HOST", default="redis"),
        "PORT": config("REDIS_PORT", default=6379),
        "DB": config("REDIS_DB", default=0),
        "PASSWORD": config("REDIS_PASSWORD", default=None),
        "DEFAULT_TIMEOUT": 360,
    },
    "high": {
        "HOST": config("REDIS_HOST", default="redis"),
        "PORT": config("REDIS_PORT", default=6379),
        "DB": config("REDIS_DB", default=0),
        "PASSWORD": config("REDIS_PASSWORD", default=None),
        "DEFAULT_TIMEOUT": 180,
    },
    "low": {
        "HOST": config("REDIS_HOST", default="redis"),
        "PORT": config("REDIS_PORT", default=6379),
        "DB": config("REDIS_DB", default=0),
        "PASSWORD": config("REDIS_PASSWORD", default=None),
        "DEFAULT_TIMEOUT": 720,
    },
}
# RQ Dashboard (optional, for monitoring)
RQ_SHOW_ADMIN_LINK = True

CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
