"""
Django settings for core project.
"""

from pathlib import Path

import os

import dj_database_url

from dotenv import load_dotenv


# --------------------------------------------------
# BASE DIRECTORY
# --------------------------------------------------

BASE_DIR = (
    Path(__file__)
    .resolve()
    .parent
    .parent
)


# --------------------------------------------------
# LOAD ENV VARIABLES
# --------------------------------------------------

load_dotenv()


# --------------------------------------------------
# SECURITY
# --------------------------------------------------

SECRET_KEY = os.getenv(
    "SECRET_KEY"
)

DEBUG = (
    os.getenv("DEBUG")
    == "True"
)

ALLOWED_HOSTS = ["*"]


# --------------------------------------------------
# APPLICATIONS
# --------------------------------------------------

INSTALLED_APPS = [

    # Django Apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third Party Apps
    "rest_framework",
    "corsheaders",

    # Local Apps
    "leads",
]


# --------------------------------------------------
# MIDDLEWARE
# --------------------------------------------------

MIDDLEWARE = [

    "django.middleware.security.SecurityMiddleware",

    "corsheaders.middleware.CorsMiddleware",

    "django.contrib.sessions.middleware.SessionMiddleware",

    "django.middleware.common.CommonMiddleware",

    "django.middleware.csrf.CsrfViewMiddleware",

    "django.contrib.auth.middleware.AuthenticationMiddleware",

    "django.contrib.messages.middleware.MessageMiddleware",

    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]


# --------------------------------------------------
# URLS / WSGI
# --------------------------------------------------

ROOT_URLCONF = "core.urls"

WSGI_APPLICATION = "core.wsgi.application"


# --------------------------------------------------
# TEMPLATES
# --------------------------------------------------

TEMPLATES = [
    {
        "BACKEND": (
            "django.template.backends."
            "django.DjangoTemplates"
        ),

        "DIRS": [
            BASE_DIR / "templates"
        ],

        "APP_DIRS": True,

        "OPTIONS": {
            "context_processors": [

                (
                    "django.template."
                    "context_processors.request"
                ),

                (
                    "django.contrib.auth."
                    "context_processors.auth"
                ),

                (
                    "django.contrib.messages."
                    "context_processors.messages"
                ),
            ],
        },
    },
]


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

DATABASES = {
    "default": (
        dj_database_url.config(
            default=os.getenv(
                "DATABASE_URL"
            )
        )
    )
}


# --------------------------------------------------
# PASSWORD VALIDATION
# --------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [

    {
        "NAME": (
            "django.contrib.auth."
            "password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },

    {
        "NAME": (
            "django.contrib.auth."
            "password_validation."
            "MinimumLengthValidator"
        ),
    },

    {
        "NAME": (
            "django.contrib.auth."
            "password_validation."
            "CommonPasswordValidator"
        ),
    },

    {
        "NAME": (
            "django.contrib.auth."
            "password_validation."
            "NumericPasswordValidator"
        ),
    },
]


# --------------------------------------------------
# INTERNATIONALIZATION
# --------------------------------------------------

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# --------------------------------------------------
# STATIC FILES
# --------------------------------------------------

STATIC_URL = "/static/"

STATIC_ROOT = (
    BASE_DIR / "staticfiles"
)


# --------------------------------------------------
# MEDIA FILES
# --------------------------------------------------

MEDIA_URL = "/media/"

MEDIA_ROOT = (
    BASE_DIR / "media"
)


# --------------------------------------------------
# DEFAULT PRIMARY KEY
# --------------------------------------------------

DEFAULT_AUTO_FIELD = (
    "django.db.models.BigAutoField"
)


# --------------------------------------------------
# CORS
# --------------------------------------------------

CORS_ALLOW_ALL_ORIGINS = True


# --------------------------------------------------
# DJANGO REST FRAMEWORK
# --------------------------------------------------

REST_FRAMEWORK = {

    "DEFAULT_RENDERER_CLASSES": [

        (
            "rest_framework.renderers."
            "JSONRenderer"
        ),
    ],

    "DEFAULT_PARSER_CLASSES": [

        (
            "rest_framework.parsers."
            "JSONParser"
        ),
    ],
}


# --------------------------------------------------
# EMAIL CONFIGURATION
# --------------------------------------------------

EMAIL_BACKEND = (
    "django.core.mail.backends."
    "smtp.EmailBackend"
)

EMAIL_HOST = os.getenv(
    "EMAIL_HOST"
)

EMAIL_PORT = os.getenv(
    "EMAIL_PORT"
)

EMAIL_HOST_USER = os.getenv(
    "EMAIL_HOST_USER"
)

EMAIL_HOST_PASSWORD = os.getenv(
    "EMAIL_HOST_PASSWORD"
)

EMAIL_USE_TLS = (
    os.getenv("EMAIL_USE_TLS")
    == "True"
)

# --------------------------------------------------
# DEFAULT EMAIL SENDER
# --------------------------------------------------

DEFAULT_FROM_EMAIL = (
    EMAIL_HOST_USER
)


# --------------------------------------------------
# FRONTEND URL (OPTIONAL)
# --------------------------------------------------

FRONTEND_URL = os.getenv(
    "FRONTEND_URL",
    "http://localhost:3000"
)

# --------------------------------------------------
# GEMINI AI
# --------------------------------------------------

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)


# --------------------------------------------------
# CELERY
# --------------------------------------------------

CELERY_BROKER_URL = os.getenv(
    "REDIS_URL"
)

CELERY_ACCEPT_CONTENT = [
    "json"
]

CELERY_TASK_SERIALIZER = (
    "json"
)

CELERY_RESULT_SERIALIZER = (
    "json"
)

CELERY_TIMEZONE = "UTC"


# --------------------------------------------------
# LOGGING
# --------------------------------------------------

LOGGING = {

    "version": 1,

    "disable_existing_loggers": False,

    "handlers": {

        "console": {
            "class": (
                "logging.StreamHandler"
            ),
        },
    },

    "root": {

        "handlers": [
            "console"
        ],

        "level": "INFO",
    },
}