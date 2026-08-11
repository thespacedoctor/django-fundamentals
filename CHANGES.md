# Changes

**v0.3.0 - August 9, 2026**

- **FEATURE:** users now choose a username at signup and can log in with
  **either** their username or their email address.
- **FEATURE:** a user settings page at `/settings/`, with tabs down the left for
  Profile, Email addresses, Change password and API. The email and password tabs
  link to allauth's own pages, which inherit the tab rail through
  `allauth/layouts/manage.html` — no per-page allauth override was added.
- **FEATURE:** profile pictures. `User.avatar` is an `ImageField` served by
  `django_fundamentals.views.AvatarView`, so uploads work with no `MEDIA_URL`
  setting and no web-server `Alias` — existing projects need no configuration
  change. Users without a picture are shown their initials everywhere an avatar
  appears.
- **FEATURE:** an API tab showing the user's DRF token, blurred by default, with
  reveal, copy-to-clipboard and a confirmed regenerate action.
- **ENHANCEMENT:** the navbar dropdown is now a rounded-square avatar linking to
  the settings page, replacing its separate email and password entries.
- **ENHANCEMENT:** new `content_outer` block in `layouts/app.html` lets a
  sub-layout wrap chrome around a page without that page cooperating. This is
  what puts the settings tabs on allauth's pages.
- **ENHANCEMENT:** new `molecules/avatar.html` component and `settings`,
  `terminal`, `eye`, `eye-off`, `copy`, `refresh` and `camera` icons.
- **REFACTOR:** `DEFAULT_SIDEBAR_NAV` no longer carries an ACCOUNT section —
  those tools live on the settings page now.

**Upgrading from v0.2.x — three things to know:**

1. **Signup now requires a username.** Existing users are unaffected: allauth had
   already auto-derived a username for each of them, so username login works
   immediately.
2. **Your sidebar will still show its ACCOUNT section.** Projects define their
   own `DJANGO_FUNDAMENTALS_SIDEBAR_NAV` in `settings.py`, which overrides the
   package default, so this is a manual edit — delete the `{"section": "Account"}`
   entry and the two entries below it.
3. **Run `python manage.py migrate`** to pick up `0002_user_avatar`, and add
   `media/` to your `.gitignore`. Pillow is now a hard dependency.

**v0.2.0 - August 9, 2026**

- **FEATURE:** full UI skeleton built from atomic-design components — app shell
  (sidebar + top navbar + footer), a separate centered layout for auth pages,
  styled 404/403/400/500 status pages, and a favicon set (SVG, ICO,
  apple-touch-icon, web manifest).
- **FEATURE:** design-token system. All colours and core dimensions are CSS
  custom properties in the host project's `static/src/tokens.css` — one file to
  re-skin the whole app. A Tailwind preset shipped in the package maps semantic
  utilities (`bg-brand`, `w-sidebar`, `text-ink`) onto them, so the mapping
  keeps updating via pip while the values stay project-owned.
- **FEATURE:** dark mode — class-based, Alpine toggle, `localStorage`-persisted,
  defaulting to `prefers-color-scheme`, with a synchronous boot script that
  avoids a flash of the wrong theme.
- **FEATURE:** data-driven sidebar via `DJANGO_FUNDAMENTALS_SIDEBAR_NAV` and
  `DJANGO_FUNDAMENTALS_SITE_NAME`, surfaced by a new
  `django_fundamentals.context_processors.design`.
- **REFACTOR:** allauth is now themed through its own extension points — its
  three layouts plus its element templates — instead of per-page overrides. All
  ~30 allauth pages are styled, including MFA/social/session flows, and allauth
  keeps its own features (social login, passkeys, login-by-code). The four
  hand-rolled `account/*.html` templates were removed as a result.
- **FIXED:** signup's "verify your email" page was unstyled — it was one of the
  many allauth templates falling through to allauth's bare layout.
- **ENHANCEMENT:** while `DEBUG` is on, the "verify your email" page shows the
  confirmation link directly, so signup can be completed without SMTP or
  digging through console output. Strictly gated on `DEBUG`.
- **DOCS:** new `ui.md` (tokens, layouts, components) and `email.md` (console
  backend in dev; Gmail SMTP with App Passwords, limits and caveats for
  production).

**v0.1.4 - August 8, 2026**

- **FIXED:** set `LOGIN_REDIRECT_URL = "/"` — Django's own default
  (`/accounts/profile/`) doesn't exist here and 404'd after every
  successful login/signup.
- **FIXED:** stop including `dj_rest_auth.registration.urls` wholesale —
  it registers `account_confirm_email` and `account_email_verification_sent`
  as empty placeholder views (by its own comment, "just to allow reverse()
  call") that shadowed allauth's real, working views of the same name,
  500ing the server-rendered signup flow's "verification email sent" page.
  Now wires only the real `RegisterView`/`VerifyEmailView`/
  `ResendEmailVerificationView` endpoints directly.
- **FIXED:** the `ACCOUNT_*`/`ANONYMOUS_USER_NAME`/`LOGIN_REDIRECT_URL`/
  `REST_AUTH` settings are now also imported in the package's own test
  settings, so the test suite exercises the same configuration a host
  project does (this is what caught the two bugs above).
- **DOCS:** quickstart/README examples now show the complete settings
  import list instead of an abbreviated one, with a note that omitting any
  of the account/auth settings silently falls back to Django/allauth
  defaults.

**v0.1.3 - August 8, 2026**

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
