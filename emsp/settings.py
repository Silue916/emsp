"""Django settings for the EMSP project."""

import os
from pathlib import Path


# --------------------------------------------------------------------------- #
#  Helpers
# --------------------------------------------------------------------------- #
def env_bool(name, default=False):
    v = os.environ.get(name)
    if v is None:
        return default
    return v.strip().lower() in {"1", "true", "yes", "y", "on"}


def env_int(name, default):
    v = os.environ.get(name)
    if v is None or not v.strip():
        return default
    try:
        return int(v)
    except ValueError:
        return default


def env_list(name, default=""):
    return [
        item.strip()
        for item in os.environ.get(name, default).split(",")
        if item.strip()
    ]


# --------------------------------------------------------------------------- #
#  Paths
# --------------------------------------------------------------------------- #
BASE_DIR = Path(__file__).resolve().parent.parent


# --------------------------------------------------------------------------- #
#  Core
# --------------------------------------------------------------------------- #
SECRET_KEY = os.environ.get(
    "DJANGO_SECRET_KEY",
    "django-insecure-6^4n&4(rj@8nyc*%d95vw50ml_8y08$11uy=n60jnx(&&jpcb^",
)

DEBUG = env_bool("DJANGO_DEBUG", True)

_allowed = env_list("DJANGO_ALLOWED_HOSTS")
ALLOWED_HOSTS = _allowed or (
    ["localhost", "127.0.0.1", "[::1]"] if DEBUG else []
)


# --------------------------------------------------------------------------- #
#  Apps
# --------------------------------------------------------------------------- #
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sitemaps",
    "accueil.apps.AccueilConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "emsp.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "accueil.context_processors.site_settings",
            ],
        },
    },
]

WSGI_APPLICATION = "emsp.wsgi.application"


# --------------------------------------------------------------------------- #
#  Database
# --------------------------------------------------------------------------- #
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# --------------------------------------------------------------------------- #
#  Auth
# --------------------------------------------------------------------------- #
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# --------------------------------------------------------------------------- #
#  I18n
# --------------------------------------------------------------------------- #
LANGUAGE_CODE = "fr-fr"
TIME_ZONE = os.environ.get("DJANGO_TIME_ZONE", "Africa/Abidjan")
USE_I18N = True
USE_TZ = True

LANGUAGES = [
    ("fr", "Français"),
    ("en", "English"),
]
LOCALE_PATHS = [BASE_DIR / "locale"]


# --------------------------------------------------------------------------- #
#  Static & media
# --------------------------------------------------------------------------- #
STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "accueil" / "static"]

MEDIA_URL = "media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# --------------------------------------------------------------------------- #
#  Auth redirects
# --------------------------------------------------------------------------- #
LOGIN_URL = "/admin/login/"
LOGIN_REDIRECT_URL = "/admin/"
LOGOUT_REDIRECT_URL = "/admin/login/"


# --------------------------------------------------------------------------- #
#  Email
# --------------------------------------------------------------------------- #
EMAIL_BACKEND = os.environ.get(
    "DJANGO_EMAIL_BACKEND",
    "django.core.mail.backends.console.EmailBackend" if DEBUG
    else "django.core.mail.backends.smtp.EmailBackend",
)
EMAIL_HOST = os.environ.get("DJANGO_EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = env_int("DJANGO_EMAIL_PORT", 587)
EMAIL_HOST_USER = os.environ.get("DJANGO_EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = os.environ.get("DJANGO_EMAIL_HOST_PASSWORD", "")
EMAIL_USE_TLS = env_bool("DJANGO_EMAIL_USE_TLS", True)
DEFAULT_FROM_EMAIL = os.environ.get(
    "DJANGO_DEFAULT_FROM_EMAIL", "EMSP <no-reply@emsp.int>"
)
CONTACT_RECIPIENT_EMAIL = os.environ.get(
    "DJANGO_CONTACT_RECIPIENT_EMAIL", "contact@emsp.int"
)
SERVER_EMAIL = DEFAULT_FROM_EMAIL


# --------------------------------------------------------------------------- #
#  Cache
# --------------------------------------------------------------------------- #
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "emsp-cache",
        "TIMEOUT": 300,
    }
}


# --------------------------------------------------------------------------- #
#  Logging
# --------------------------------------------------------------------------- #
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO" if not DEBUG else "DEBUG",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}


# --------------------------------------------------------------------------- #
#  Security (production)
# --------------------------------------------------------------------------- #
_csrf_trusted = env_list("DJANGO_CSRF_TRUSTED_ORIGINS")
if _csrf_trusted:
    CSRF_TRUSTED_ORIGINS = _csrf_trusted

if not DEBUG:
    SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", True)
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = env_int("DJANGO_SECURE_HSTS_SECONDS", 31536000)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = env_bool("DJANGO_SECURE_HSTS_PRELOAD", False)
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "same-origin"
    X_FRAME_OPTIONS = "DENY"


# --------------------------------------------------------------------------- #
#  File upload limits
# --------------------------------------------------------------------------- #
DATA_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10 MB
