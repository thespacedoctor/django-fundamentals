from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import NoReverseMatch, reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, UpdateView

from django_fundamentals.forms import ProfileForm

# HOW LONG A BROWSER MAY CACHE AN AVATAR. PRIVATE BECAUSE AvatarView REQUIRES
# AUTHENTICATION — A SHARED PROXY MUST NOT HAND ONE USER'S AVATAR TO ANOTHER.
AVATAR_CACHE_SECONDS = 60 * 60 * 24

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


class SettingsProfileView(LoginRequiredMixin, UpdateView):
    """*the Profile tab — username, real name and profile picture*

    **Usage:**

    ```python
    path("settings/profile/", SettingsProfileView.as_view(), name="django_fundamentals_settings")
    ```
    """

    form_class = ProfileForm
    template_name = "django_fundamentals/settings_profile.html"
    success_url = reverse_lazy("django_fundamentals_settings")

    def get_object(self, queryset=None):
        """*a user may only ever edit themselves*

        **Return:**

        - ``user`` -- the signed-in user

        **Usage:**

        ```python
        targetUser = self.get_object()
        ```
        """
        return self.request.user

    def form_valid(self, form):
        messages.success(self.request, "Profile updated.")
        return super().form_valid(form)


class SettingsApiView(LoginRequiredMixin, TemplateView):
    """*the API tab — view, copy and regenerate the user's DRF token*"""

    template_name = "django_fundamentals/settings_api.html"

    def get_context_data(self, **kwargs):
        from rest_framework.authtoken.models import Token

        context = super().get_context_data(**kwargs)
        # get_or_create SO A USER WHO SIGNED UP BEFORE EVER CALLING THE API
        # STILL SEES A TOKEN RATHER THAN AN EMPTY BOX
        apiToken, _ = Token.objects.get_or_create(user=self.request.user)
        context["api_token"] = apiToken
        return context


class ApiTokenRegenerateView(LoginRequiredMixin, View):
    """*replace the signed-in user's API token with a fresh one*

    POST only. DRF's ``authtoken`` is strictly one token per user, so this is
    destructive: the previous key stops authenticating the moment it is
    deleted. The template confirms before posting here.
    """

    def post(self, request, *args, **kwargs):
        from rest_framework.authtoken.models import Token

        Token.objects.filter(user=request.user).delete()
        Token.objects.create(user=request.user)
        messages.success(
            request, "API token regenerated. The previous token no longer works."
        )
        return redirect("django_fundamentals_settings_api")


class AvatarView(LoginRequiredMixin, View):
    """*stream a user's profile picture*

    Avatars are served by Django rather than by the web server so that
    projects generated before this feature existed pick it up from
    ``pip install -U django-fundamentals`` alone — there is no ``MEDIA_URL``
    to add and no Apache ``Alias`` to deploy. Files are small and cached hard,
    so the cost of a Python request per avatar is acceptable.

    **Usage:**

    ```django
    <img src="{% url 'django_fundamentals_avatar' user.pk %}">
    ```
    """

    def get(self, request, *args, **kwargs):
        from django.contrib.auth import get_user_model

        targetUser = get_object_or_404(get_user_model(), pk=kwargs["pk"])
        if not targetUser.avatar:
            raise Http404("This user has no profile picture.")

        try:
            avatarFile = targetUser.avatar.open("rb")
        except FileNotFoundError:
            # THE DB ROW SURVIVED BUT THE FILE DIDN'T (RESTORED DUMP, MOVED
            # MEDIA DIR). 404 SO THE TEMPLATE FALLS BACK TO INITIALS.
            raise Http404("Profile picture is missing from storage.")

        response = FileResponse(avatarFile)
        response["Cache-Control"] = f"private, max-age={AVATAR_CACHE_SECONDS}"
        return response
