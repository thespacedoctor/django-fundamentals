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

from django_fundamentals.views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="django_fundamentals_home"),
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
