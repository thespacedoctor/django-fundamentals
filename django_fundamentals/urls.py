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

from django.urls import include, path

urlpatterns = [
    path("accounts/", include("allauth.urls")),
    path("api/auth/", include("dj_rest_auth.urls")),
    path("api/auth/registration/", include("dj_rest_auth.registration.urls")),
]
