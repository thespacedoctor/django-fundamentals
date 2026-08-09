# Usage

## The 4-tier authorization model

| Tier | Django mechanism | Access |
|---|---|---|
| 1. Anonymous | `AnonymousUser` (built-in) | Read-only access to public content |
| 2. Authenticated | `is_active=True` + Groups/Permissions | Create/edit/delete their own content only |
| 3. Staff | `is_staff=True` | Django admin access |
| 4. Superuser | `is_superuser=True` | Bypasses all permission checks |

`django_fundamentals.permissions` provides the building blocks:

- `IsOwnerOrReadOnly` — DRF permission, tier 2 (object must expose `owner`).
- `IsStaffUser` / `IsSuperUser` — DRF permissions, tiers 3/4.
- `StaffRequiredMixin` / `SuperuserRequiredMixin` — Django class-based-view mixins, tiers 3/4.
- `assign_owner_permissions(user, obj)` — grants guardian view/change/delete object permissions to the owner of a newly created object.

```python
from django_fundamentals.permissions import IsOwnerOrReadOnly, assign_owner_permissions

class WidgetViewSet(viewsets.ModelViewSet):
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        widget = serializer.save(owner=self.request.user)
        assign_owner_permissions(self.request.user, widget)
```

## Homepage

`django_fundamentals.urls` wires up `path("", HomeView.as_view(), name="django_fundamentals_home")`
as its first entry — a simple page listing the URLs the package has already
added (login, signup, password reset, the dj-rest-auth API endpoints, etc.),
so a freshly generated project doesn't 404 at `/`. Two ways to override it:

- **Template override** — add your own
  `templates/django_fundamentals/home.html` (see "Overriding templates"
  below); the built-in `HomeView` still supplies the `homepage_urls` context.
- **Full replacement** — define your own `path("", ...)` **above**
  `include("django_fundamentals.urls")` in your project's `urls.py`; Django's
  resolver matches the first pattern, so your view wins entirely.

## Overriding templates

The UI skeleton's layouts and components live under
`django_fundamentals/templates/django_fundamentals/`. A host project can
override any of them by placing a same-named file at the equivalent path in
its own `templates/` directory, as long as that directory is listed before
`django_fundamentals` in `INSTALLED_APPS`/`DIRS`.

allauth is themed through its own extension points — its three layouts and its
element templates, overridden at
`django_fundamentals/templates/allauth/`. This package is listed **before**
`allauth.account` in `BASE_INSTALLED_APPS` so those overrides take precedence.

See [UI skeleton](ui.md) for the full component list and the design tokens.

## Management commands

- `create_superuser_if_none` — creates a superuser from
  `DJANGO_SUPERUSER_USERNAME` / `_EMAIL` / `_PASSWORD` env vars if no
  superuser exists yet. Safe to run on every deploy.
