"""*minimal Django settings used only to run this package's own test suite*"""

from django_fundamentals.settings import (
    ACCOUNT_ADAPTER,
    ACCOUNT_EMAIL_VERIFICATION,
    ACCOUNT_LOGIN_METHODS,
    ACCOUNT_LOGOUT_REDIRECT_URL,
    ACCOUNT_SIGNUP_FIELDS,
    ACCOUNT_UNIQUE_EMAIL,
    ANONYMOUS_USER_NAME,
    BASE_AUTHENTICATION_BACKENDS,
    BASE_INSTALLED_APPS,
    BASE_MIDDLEWARE,
    BASE_REST_FRAMEWORK,
    BASE_TEMPLATE_CONTEXT_PROCESSORS,
    LOGIN_REDIRECT_URL,
    REST_AUTH,
)

SECRET_KEY = "test-secret-key-not-for-production"
DEBUG = True
ALLOWED_HOSTS = ["*"]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

INSTALLED_APPS = [*BASE_INSTALLED_APPS, "django_fundamentals.tests.testapp"]
MIDDLEWARE = BASE_MIDDLEWARE
AUTHENTICATION_BACKENDS = BASE_AUTHENTICATION_BACKENDS
REST_FRAMEWORK = BASE_REST_FRAMEWORK

AUTH_USER_MODEL = "django_fundamentals.User"
ROOT_URLCONF = "django_fundamentals.tests.urls"
SITE_ID = 1
STATIC_URL = "/static/"
USE_TZ = True
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": BASE_TEMPLATE_CONTEXT_PROCESSORS},
    }
]
