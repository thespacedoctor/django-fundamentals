"""*includable URLconf: server-rendered allauth views plus dj-rest-auth API endpoints*

**Usage:**

```python
# project urls.py
from django.urls import include, path

urlpatterns = [
    path("", include("django_fundamentals.urls")),
]
```
"""

from dj_rest_auth.registration.views import (
    RegisterView,
    ResendEmailVerificationView,
    VerifyEmailView,
)
from django.urls import include, path
from django.views.generic import RedirectView

from django_fundamentals.views import (
    ApiTokenRegenerateView,
    AvatarView,
    HomeView,
    SettingsApiView,
    SettingsProfileView,
)

urlpatterns = [
    path("", HomeView.as_view(), name="django_fundamentals_home"),
    # USER SETTINGS. THE AVATAR ROUTE SHARES allauth's accounts/ PREFIX AND IS
    # DECLARED ABOVE include("allauth.urls") SO IT KEEPS WINNING IF allauth EVER
    # ADDS A PATTERN THAT WOULD SWALLOW IT.
    path(
        "settings/",
        RedirectView.as_view(pattern_name="django_fundamentals_settings", permanent=False),
        name="django_fundamentals_settings_index",
    ),
    path(
        "settings/profile/",
        SettingsProfileView.as_view(),
        name="django_fundamentals_settings",
    ),
    path(
        "settings/api/",
        SettingsApiView.as_view(),
        name="django_fundamentals_settings_api",
    ),
    path(
        "settings/api/token/regenerate/",
        ApiTokenRegenerateView.as_view(),
        name="django_fundamentals_token_regenerate",
    ),
    path(
        "accounts/avatar/<int:pk>/",
        AvatarView.as_view(),
        name="django_fundamentals_avatar",
    ),
    path("accounts/", include("allauth.urls")),
    path("api/auth/", include("dj_rest_auth.urls")),
    # WIRED UP EXPLICITLY RATHER THAN VIA include("dj_rest_auth.registration.urls"):
    # THAT MODULE ALSO REGISTERS "account_confirm_email" AND
    # "account_email_verification_sent" AS EMPTY PLACEHOLDER TemplateViews (ITS OWN
    # COMMENT: "just to allow reverse() call"), WHICH COLLIDE WITH — AND SHADOW —
    # allauth's REAL, WORKING VIEWS OF THE SAME NAME, 500ING THE SERVER-RENDERED
    # SIGNUP FLOW'S "VERIFICATION EMAIL SENT" PAGE. SKIPPING THOSE TWO PATTERNS
    # LEAVES allauth's OWN VERSIONS AS THE ONLY ONES REGISTERED.
    path("api/auth/registration/", RegisterView.as_view(), name="rest_register"),
    path(
        "api/auth/registration/verify-email/",
        VerifyEmailView.as_view(),
        name="rest_verify_email",
    ),
    path(
        "api/auth/registration/resend-email/",
        ResendEmailVerificationView.as_view(),
        name="rest_resend_email",
    ),
]
