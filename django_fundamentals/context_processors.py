"""*context processors making design/chrome settings available to every template*"""

from django.conf import settings

# SENSIBLE DEFAULT NAV — PROJECTS REPLACE THIS WHOLESALE VIA THE
# DJANGO_FUNDAMENTALS_SIDEBAR_NAV SETTING. AN ENTRY WITH A "section" KEY IS A
# GROUP HEADING RATHER THAN A LINK.
DEFAULT_SIDEBAR_NAV = [
    {"label": "Home", "url_name": "django_fundamentals_home", "icon": "home"},
]

# THE SETTINGS PAGE TAB RAIL. SUPPLIED TO EVERY TEMPLATE RATHER THAN BUILT IN A
# VIEW BECAUSE TWO OF THESE TABS RENDER ON allauth's OWN PAGES, WHICH USE
# allauth's VIEWS — THERE IS NO get_context_data OF OURS TO HOOK.
SETTINGS_TABS = [
    {"label": "Profile", "url_name": "django_fundamentals_settings", "icon": "user"},
    {"label": "Email addresses", "url_name": "account_email", "icon": "mail"},
    {"label": "Change password", "url_name": "account_change_password", "icon": "key"},
    {"label": "API", "url_name": "django_fundamentals_settings_api", "icon": "terminal"},
]


def design(request):
    """*expose site chrome settings (name, sidebar nav, version) to all templates*

    Added to ``BASE_TEMPLATE_CONTEXT_PROCESSORS`` so it reaches host projects
    automatically on upgrade.

    **Key Arguments:**

    - ``request`` -- the current request

    **Return:**

    - ``context`` -- dict of ``df_``-prefixed template variables

    **Usage:**

    ```django
    {{ df_site_name }}
    {% for item in df_sidebar_nav %}...{% endfor %}
    ```
    """
    from django_fundamentals import __version__
    from django_fundamentals.adapters import DEV_CONFIRMATION_URL_SESSION_KEY

    context = {
        "df_site_name": getattr(settings, "DJANGO_FUNDAMENTALS_SITE_NAME", "Django Fundamentals"),
        "df_sidebar_nav": getattr(
            settings, "DJANGO_FUNDAMENTALS_SIDEBAR_NAV", DEFAULT_SIDEBAR_NAV
        ),
        "df_settings_tabs": SETTINGS_TABS,
        "df_version": __version__,
    }

    # DEVELOPMENT-ONLY: SURFACE THE LAST EMAIL-CONFIRMATION LINK SO THE
    # "verification sent" PAGE CAN SHOW IT WHEN THERE IS NO SMTP SERVER.
    # READ, NOT POPPED, SO REFRESHING THAT PAGE STILL WORKS.
    if settings.DEBUG and hasattr(request, "session"):
        context["df_dev_confirmation_url"] = request.session.get(
            DEV_CONFIRMATION_URL_SESSION_KEY
        )

    return context
