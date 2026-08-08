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

## Overriding templates

`base.html`, `nav.html`, and `footer.html` live under
`django_fundamentals/templates/django_fundamentals/`. A host project can
override any of them by placing a same-named file at the equivalent path in
its own `templates/` directory, as long as that directory is listed before
`django_fundamentals` in `INSTALLED_APPS`/`DIRS`.

allauth's own templates (`account/login.html`, `account/signup.html`, etc.)
are overridden directly at `django_fundamentals/templates/account/` — this
package is listed **before** `allauth.account` in `BASE_INSTALLED_APPS` so
these overrides take precedence.

## Management commands

- `create_superuser_if_none` — creates a superuser from
  `DJANGO_SUPERUSER_USERNAME` / `_EMAIL` / `_PASSWORD` env vars if no
  superuser exists yet. Safe to run on every deploy.
