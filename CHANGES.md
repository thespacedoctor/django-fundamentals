# Changes

**Unreleased**

- **FEATURE:** default homepage at `/` (`HomeView`) listing the URLs
  django-fundamentals has already wired up, with a short description of
  each. Overridable via a `templates/django_fundamentals/home.html`
  template, or fully replaceable with a project's own `path("", ...)`.
- **DOCS:** install instructions now suggest creating and activating an
  isolated conda environment (`conda create -n django-fundamentals pip -c
  conda-forge`) before `pip install`.

**v0.1.2 - August 8, 2026**

- **FIXED:** revert a footer smoke-test artifact left over from verifying
  update propagation end-to-end (no functional change).

**v0.1.1 - August 8, 2026**

- **FIXED:** declare `requests` as a direct dependency —
  `dj_rest_auth.registration` unconditionally imports allauth's oauth2
  client, which needs it even with no social provider configured.
- **FIXED:** `create_superuser_if_none` now pre-verifies the bootstrap
  superuser's `EmailAddress` so they can log in immediately under
  `ACCOUNT_EMAIL_VERIFICATION = "mandatory"`, without needing SMTP
  configured yet.

**v0.1.0 - August 8, 2026**

- **FEATURE:** initial release. Custom `User` model, allauth + dj-rest-auth
  wiring, guardian-based object-level permissions, 4-tier authorization
  helpers, HTMX + Alpine.js + Tailwind base templates and static assets.
