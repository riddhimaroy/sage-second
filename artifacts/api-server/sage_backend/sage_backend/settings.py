"""
Django settings for SAGE - Smart Nutrition Tracker.
"""

import os
import dj_database_url
from pathlib import Path

# Build paths inside the project
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY
SECRET_KEY = os.environ.get("DJANGO_SECRET_KEY", "sage-dev-secret-key-change-in-production")
DEBUG = os.environ.get("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    "django.contrib.contenttypes",
    "django.contrib.auth",          # Required by Django REST Framework
    "django.contrib.staticfiles",
    "rest_framework",               # Django REST Framework
    "rest_framework.authtoken",     # Token-based authentication
    "corsheaders",                  # CORS headers for React frontend
    "meals",                        # Meals app: Meal model, search/list endpoints
    "logs",                         # Logs app: DailyLog, LogEntry, weekly summary
    "users",                        # Users app: registration, login, profile
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",   # Must be before CommonMiddleware
    "django.middleware.security.SecurityMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "sage_backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = "sage_backend.wsgi.application"

# Database — use PostgreSQL via DATABASE_URL env var
DATABASE_URL = os.environ.get("DATABASE_URL", "")
if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }
else:
    # Fallback to SQLite for local development without DATABASE_URL
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

# Static files
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Django REST Framework configuration
REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.AllowAny",
    ],
}

# CORS — allow the React frontend to call the API
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "x-requested-with",
]

# Internationalization
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True
