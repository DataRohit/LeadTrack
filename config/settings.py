# ruff: noqa: E501

# Imports
import ssl
from pathlib import Path

import environ

# Base directory of the Django project
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent

# App directory of the Django project
APPS_DIR = BASE_DIR / "apps"

# Initialize environment variables
env = environ.Env()

# General
# ------------------------------------------------------------------------------
DEBUG = env.bool("DJANGO_DEBUG", default=False)
SECRET_KEY = env(
    "DJANGO_SECRET_KEY", default="0939f=2n4l)hb+o(@wpxp)_)ihxiv$7$6mxp1rx6fcu=^+(l+f"
)
ALLOWED_HOSTS = env.list("DJANGO_ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])
CSRF_TRUSTED_ORIGINS = env.list(
    "DJANGO_CSRF_TRUSTED_ORIGINS",
    default=["http://localhost:8080", "http://127.0.0.1:8080"],
)

# Internationalization
# ------------------------------------------------------------------------------
TIME_ZONE = "Asia/Kolkata"
LANGUAGE_CODE = "en-us"
USE_I18N = True
USE_TZ = True
LOCALE_PATHS = [str(BASE_DIR / "locale")]

# Site settings
# ------------------------------------------------------------------------------
SITE_ID = 1
SITE_NAME = env("SITE_NAME", default="LeadTrack")

# Databases
# ------------------------------------------------------------------------------
DATABASES = {"default": env.db("DATABASE_URL", default="sqlite:///db.sqlite3")}
DATABASES["default"]["ENGINE"] = env.str(
    "DATABASE_ENGINE", default="django.db.backends.sqlite3"
)
DATABASES["default"]["ATOMIC_REQUESTS"] = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Urls
# ------------------------------------------------------------------------------
ROOT_URLCONF = "config.urls"
WSGI_APPLICATION = "config.wsgi.application"

# Apps
# ------------------------------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    "django.forms",
]
THIRD_PARTY_APPS = [
    "django_extensions",
    "storages",
    "djcelery_email",
    "corsheaders",
]
LOCAL_APPS = []
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Authentication
# ------------------------------------------------------------------------------
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# Migrations
# ------------------------------------------------------------------------------
MIGRATION_MODULES = {"sites": "apps.contrib.sites.migrations"}

# Passwords
# ------------------------------------------------------------------------------
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# Middleware
# ------------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# Session Settings
# ------------------------------------------------------------------------------
SESSION_COOKIE_AGE = 21600
SESSION_EXPIRE_AT_BROWSER_CLOSE = env.bool(
    "SESSION_EXPIRE_AT_BROWSER_CLOSE", default=False
)

# Templates
# ------------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(APPS_DIR / "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                "django.template.context_processors.static",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# Admin
# ------------------------------------------------------------------------------
ADMIN_URL = env("ADMIN_URL", default="admin/")
ADMINS = [("""Rohit Vilas Ingole""", "rohit.vilas.ingole@gmail.com")]
MANAGERS = ADMINS

# Logging
# ------------------------------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s",
        },
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {"level": "INFO", "handlers": ["console"]},
}

# MinIO
# ------------------------------------------------------------------------------
MINIO_STORAGE_ENDPOINT = env("MINIO_STORAGE_ENDPOINT", default="localhost:9000")
MINIO_STORAGE_ACCESS_KEY = env("MINIO_STORAGE_ACCESS_KEY")
MINIO_STORAGE_SECRET_KEY = env("MINIO_STORAGE_SECRET_KEY")
MINIO_STORAGE_DOMAIN = env("MINIO_STORAGE_DOMAIN", default="localhost:8080")
MINIO_STORAGE_USE_HTTPS = False

# AWS S3
# ------------------------------------------------------------------------------
AWS_S3_ENDPOINT_URL = f"http://{MINIO_STORAGE_ENDPOINT}"
AWS_ACCESS_KEY_ID = MINIO_STORAGE_ACCESS_KEY
AWS_SECRET_ACCESS_KEY = MINIO_STORAGE_SECRET_KEY
AWS_STORAGE_BUCKET_NAME = env("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION_NAME = "us-east-1"
AWS_S3_SIGNATURE_VERSION = "s3v4"
AWS_DEFAULT_ACL = "private"
AWS_S3_FILE_OVERWRITE = False
AWS_QUERYSTRING_AUTH = True
AWS_S3_CUSTOM_DOMAIN = f"{MINIO_STORAGE_DOMAIN}/minio/storage/{AWS_STORAGE_BUCKET_NAME}"

# Static files settings
# ------------------------------------------------------------------------------
STATIC_URL = f"http://{MINIO_STORAGE_DOMAIN}/{AWS_STORAGE_BUCKET_NAME}/static/"
STATICFILES_STORAGE = "config.storage.static.StaticStorage"

# Media files settings
# ------------------------------------------------------------------------------
MEDIA_URL = f"http://{MINIO_STORAGE_DOMAIN}/{AWS_STORAGE_BUCKET_NAME}/media/"
DEFAULT_FILE_STORAGE = "config.storage.media.MediaStorage"

# Static files finders and directories
# ------------------------------------------------------------------------------
STATICFILES_DIRS = [str(APPS_DIR / "static")]
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# Redis
# ------------------------------------------------------------------------------
REDIS_URL = env.str("REDIS_URL", default="redis://redis-service:6379/")
REDIS_SSL = REDIS_URL.startswith("rediss://")

# Caches
# ------------------------------------------------------------------------------
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": REDIS_URL,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "KEY_PREFIX": "leadtrack",
            "TIMEOUT": 900,
        },
    }
}

# Celery
# ------------------------------------------------------------------------------
if USE_TZ:
    CELERY_TIMEZONE = TIME_ZONE
CELERY_BROKER_URL = env("CELERY_BROKER_URL")
CELERY_BROKER_USE_SSL = {"ssl_cert_reqs": ssl.CERT_NONE} if REDIS_SSL else None
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_RESULT_EXTENDED = True
CELERY_RESULT_BACKEND_ALWAYS_RETRY = True
CELERY_RESULT_BACKEND_MAX_RETRIES = 10
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TASK_TIME_LIMIT = 5 * 60
CELERY_TASK_SOFT_TIME_LIMIT = 60
CELERY_WORKER_SEND_TASK_EVENTS = True
CELERY_TASK_SEND_SENT_EVENT = True
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_EMAIL_TASK_CONFIG = {
    "rate_limit": "50/m",
    "ignore_result": True,
}

# Email
# ------------------------------------------------------------------------------
EMAIL_BACKEND = env.str(
    "DJANGO_EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)
EMAIL_HOST = env("DJANGO_EMAIL_HOST")
EMAIL_PORT = env("DJANGO_EMAIL_PORT")
DEFAULT_FROM_EMAIL = env("DJANGO_DEFAULT_FROM_EMAIL")
EMAIL_TIMEOUT = 5

# Django CORS Headers
# -------------------------------------------------------------------------------
CORS_URLS_REGEX = r"^/api/.*$"
