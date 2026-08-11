"""*building blocks a host project merges into its own ``settings.py``*

The ``BASE_*`` names are plain lists/dicts a host project splices into its
own ``INSTALLED_APPS`` etc. so it keeps full control over ordering. The
rest (``ACCOUNT_*``, ``ANONYMOUS_USER_NAME``, ``LOGIN_REDIRECT_URL``,
``REST_AUTH``) are real Django/allauth/guardian settings values — importing
them into a settings module's namespace is enough for Django to pick them
up, no reassignment needed. Leaving any of these out silently falls back to
Django/allauth's own defaults, so import all of them. See
``docs/source/quickstart.md`` for the full example.
"""

BASE_INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.sites",
    # LISTED BEFORE allauth.account SO ITS account/*.html OVERRIDES TAKE PRECEDENCE
    # (Django's app_directories template loader resolves in INSTALLED_APPS order)
    "django_fundamentals",
    "rest_framework",
    "rest_framework.authtoken",
    "allauth",
    "allauth.account",
    # dj_rest_auth.registration UNCONDITIONALLY IMPORTS allauth.socialaccount MODELS,
    # SO IT MUST BE INSTALLED EVEN IF NO SOCIAL PROVIDERS ARE CONFIGURED
    "allauth.socialaccount",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "guardian",
]

BASE_MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

BASE_AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
    "guardian.backends.ObjectPermissionBackend",
]

BASE_REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",
    ],
}

BASE_TEMPLATE_CONTEXT_PROCESSORS = [
    "django.template.context_processors.debug",
    "django.template.context_processors.request",
    "django.contrib.auth.context_processors.auth",
    "django.contrib.messages.context_processors.messages",
    # SUPPLIES df_site_name / df_sidebar_nav / df_version TO THE UI SKELETON
    "django_fundamentals.context_processors.design",
]

# GUARDIAN NEEDS AN ANONYMOUS USER NAME FOR OBJECT-LEVEL PERMISSION CHECKS
ANONYMOUS_USER_NAME = None

# ALLAUTH DEFAULTS TUNED FOR AN API-FIRST (DJ-REST-AUTH) PROJECT.
# BOTH allauth's LoginForm AND dj-rest-auth's LoginSerializer BRANCH ON
# ACCOUNT_LOGIN_METHODS, SO ACCEPTING EITHER IDENTIFIER NEEDS NO CUSTOM FORM.
ACCOUNT_LOGIN_METHODS = {"email", "username"}
# USERNAME IS COLLECTED EXPLICITLY RATHER THAN LEFT TO allauth's
# populate_username(), WHICH DERIVES AN OPAQUE VALUE FROM THE EMAIL — USERS
# CAN'T LOG IN WITH A USERNAME THEY WERE NEVER SHOWN.
ACCOUNT_SIGNUP_FIELDS = ["username*", "email*", "password1*", "password2*"]
ACCOUNT_EMAIL_VERIFICATION = "mandatory"
ACCOUNT_UNIQUE_EMAIL = True

# ADDS A DEBUG-ONLY CONVENIENCE: STASHES THE EMAIL-CONFIRMATION LINK SO THE
# "verification sent" PAGE CAN DISPLAY IT WHEN NO SMTP SERVER IS CONFIGURED.
# INERT OUTSIDE DEBUG — SEE django_fundamentals/adapters.py
ACCOUNT_ADAPTER = "django_fundamentals.adapters.AccountAdapter"

# DJANGO'S OWN DEFAULT ("/accounts/profile/") DOESN'T EXIST HERE — SEND USERS
# TO THE django_fundamentals HOMEPAGE AFTER LOGIN/LOGOUT INSTEAD
LOGIN_REDIRECT_URL = "/"
ACCOUNT_LOGOUT_REDIRECT_URL = "/"

REST_AUTH = {
    "USE_JWT": False,
    "SESSION_LOGIN": True,
}

# --- UI SKELETON -----------------------------------------------------------
# THESE ARE READ BY django_fundamentals.context_processors.design VIA
# getattr(settings, ...), SO A HOST PROJECT OVERRIDES THEM SIMPLY BY DEFINING
# ITS OWN VALUE IN settings.py — THERE IS NOTHING TO IMPORT FOR THESE TWO.
#
#   DJANGO_FUNDAMENTALS_SITE_NAME    -- shown in <title>, brand mark, footer
#   DJANGO_FUNDAMENTALS_SIDEBAR_NAV  -- list of {label, url_name, icon} dicts,
#                                       or {section: "..."} for a group heading.
#                                       Defaults to DEFAULT_SIDEBAR_NAV in
#                                       django_fundamentals/context_processors.py
