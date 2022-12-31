"""
Django settings for test project.

Generated by 'django-admin startproject' using Django 4.1.1.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from django.utils import timezone

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# for context processor
BASE_HTML = "django_messages/base.html"
SITE_NAME = "django_messages"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-1*lgqsqmt50224cmputddn-v+^k1d+zf$9rjhp^d+mqirdg!p*"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]


# Application definition

INSTALLED_APPS = [
    # "debug_toolbar",
    "django_messages",
    "django_q",
    "django_redis",
    "crispy_forms",
    "crispy_bootstrap5",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    # "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "django_messages.testapp.urls"

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
                "django_messages.context_processors.base_html",
                "django_messages.context_processors.site_name",
            ],
        },
    },
]

# WSGI_APPLICATION = "test.wsgi.application"

# debug toolbar
INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
        "TEST": {
            "NAME": "testdb.sqlite3",
        },
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

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# crispy bootstrap
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"


CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

# django-q
Q_CLUSTER = {
    "name": "DJRedis",
    "workers": 4,
    "timeout": 20,
    "retry": 60,
    "django_redis": "default",
}


# settings for bleach

ALLOWED_TAGS = [
    "a",
    "div",
    "p",
    "span",
    "img",
    "em",
    "i",
    "li",
    "ol",
    "ul",
    "strong",
    "br",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "table",
    "tbody",
    "thead",
    "tr",
    "td",
    "abbr",
    "acronym",
    "b",
    "blockquote",
    "code",
    "strike",
    "u",
    "sup",
    "sub",
]

from bleach.css_sanitizer import CSSSanitizer

CSS_SANITIZER = CSSSanitizer(
    allowed_css_properties=[
        "background-color",
        "font-size",
        "line-height",
        "color",
        "font-family",
    ]
)

ATTRIBUTES = {
    "*": [
        "style",
        "align",
        "color",
    ],
    "a": [
        "href",
    ],
}

# softdeletion params

DELETION_TIMEOUT = {
    "POST": timezone.timedelta(days=21),
    "COMMENT": timezone.timedelta(days=14),
}


# django messages
NUMBER_OF_MESSAGES_PER_PAGE = 6
ABSTRACTMESSAGE = False
