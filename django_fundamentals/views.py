from django.urls import NoReverseMatch, reverse
from django.views.generic import TemplateView

# (URL NAME, SHORT DESCRIPTION) — RESOLVED VIA reverse() SO PATHS STAY CORRECT
# IF PREFIXES EVER CHANGE. NAMES THAT FAIL TO RESOLVE ARE SILENTLY SKIPPED.
HOMEPAGE_URLS = [
    ("account_login", "Log in (server-rendered)"),
    ("account_signup", "Sign up (server-rendered)"),
    ("account_logout", "Log out"),
    ("account_email", "Manage email addresses"),
    ("account_reset_password", "Request a password reset email"),
    ("rest_login", "API: log in"),
    ("rest_logout", "API: log out"),
    ("rest_register", "API: register a new account"),
    ("rest_verify_email", "API: verify an email address"),
    ("rest_user_details", "API: view/update the current user"),
    ("rest_password_reset", "API: request a password reset"),
    ("rest_password_reset_confirm", "API: confirm a password reset"),
]


class HomeView(TemplateView):
    """*default django-fundamentals homepage — lists the URLs this package has already wired up*

    Override by placing a template at the same relative path
    (``django_fundamentals/home.html``) in a host project's own templates
    directory, or replace this view entirely by defining a project's own
    ``path("", ...)`` above ``include("django_fundamentals.urls")``.
    """

    template_name = "django_fundamentals/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        resolvedUrls = []
        for urlName, description in HOMEPAGE_URLS:
            try:
                resolvedUrls.append({"path": reverse(urlName), "description": description})
            except NoReverseMatch:
                continue
        context["homepage_urls"] = resolvedUrls
        return context
