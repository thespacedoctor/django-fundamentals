# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

`django-fundamentals` is a **reusable Django app distributed on PyPI** — not a
website. There is no `manage.py`, no project `settings.py`, and nothing to
`runserver`. It is consumed two ways:

1. New projects are generated from
   [django-fundamentals-cookiecutter](https://github.com/thespacedoctor/django-fundamentals-cookiecutter),
   which pins this package as a dependency.
2. Existing generated projects pick up changes via `pip install -U django-fundamentals`.

That second path drives most design decisions here: **anything that should
reach existing apps on upgrade must live inside the package**, and anything the
project owns (token *values*, `tailwind.config.js`, `package.json`) must stay
out of it. See the header comment in
`django_fundamentals/static/django_fundamentals/tailwind-preset.js` for the
canonical statement of this split.

The only executable Django configuration in the repo is
`django_fundamentals/tests/settings.py` + `tests/urls.py` — a minimal host
project that exists solely so the test suite exercises the package the same way
a real project does.

## Commands

The repo has a local `.venv` (Python 3.14, Django 5.2). README/docs recommend a
conda env instead; either works.

```bash
pip install -e ".[dev]"          # dev == tests + docs + build + twine

pytest                           # full suite (42 tests, ~2s, in-memory sqlite)
pytest django_fundamentals/tests/test_ui.py                     # one file
pytest django_fundamentals/tests/test_ui.py::test_nav_url_returns_empty_for_unknown_name   # one test
pytest -q --cov=django_fundamentals                             # with coverage

sphinx-build -b html docs/source docs/build     # docs (also built by Read the Docs)
python -m build                                 # sdist + wheel
```

`pytest.ini` sets `DJANGO_SETTINGS_MODULE=django_fundamentals.tests.settings`,
so no `--ds` flag is needed. CI (`.github/workflows/assest/integration-tests.sh`
— the directory typo is deliberate, it matches the reusable workflow) runs
`pip install -e ".[tests]" && pytest -q`.

**Releasing:** version comes from git tags via setuptools-scm (writing the
gitignored `django_fundamentals/__version__.py`). Pushing a `v*` tag triggers
`.github/workflows/publish.yml` → PyPI + a GitHub Release whose body is the tag
message. Add the release entry to `CHANGES.md` first.

## Architecture

### Settings are importable constants, not a settings module

`django_fundamentals/settings.py` exports two kinds of name and the distinction
matters:

- `BASE_INSTALLED_APPS`, `BASE_MIDDLEWARE`, `BASE_AUTHENTICATION_BACKENDS`,
  `BASE_REST_FRAMEWORK`, `BASE_TEMPLATE_CONTEXT_PROCESSORS` — plain
  lists/dicts a host project **splices into** its own settings, keeping control
  of ordering.
- `ACCOUNT_*`, `ANONYMOUS_USER_NAME`, `LOGIN_REDIRECT_URL`, `REST_AUTH` — real
  setting values that take effect **merely by being imported** into a settings
  module's namespace. Omitting one silently falls back to a Django/allauth
  default, which is how the v0.1.4 post-login 404 happened. When adding a
  setting here, also add it to `django_fundamentals/tests/settings.py` and to
  the import list in `docs/source/quickstart.md` and `README.md`.
- `DJANGO_FUNDAMENTALS_SITE_NAME` / `DJANGO_FUNDAMENTALS_SIDEBAR_NAV` are the
  exception: read via `getattr(settings, ...)` in `context_processors.py`, so a
  project overrides them by simply defining them — there is nothing to import.

Ordering constraint: `django_fundamentals` is listed **before** `allauth.account`
in `BASE_INSTALLED_APPS` so its `templates/allauth/**` overrides win under
Django's app-directories loader. `allauth.socialaccount` is installed
unconditionally because `dj_rest_auth.registration` imports its models.

### URLs

`django_fundamentals/urls.py` deliberately does **not**
`include("dj_rest_auth.registration.urls")` — that module registers
`account_confirm_email` and `account_email_verification_sent` as empty
placeholder views that shadow allauth's real ones and 500 the server-rendered
signup flow. The three real registration views are wired individually instead.
Do not "simplify" this back into an `include()`.

### Authorization

`permissions.py` implements the 4-tier model (Anonymous / Authenticated / Staff
/ Superuser) as DRF permission classes plus CBV mixins, with guardian supplying
object-level permissions (`assign_owner_permissions`). `docs/source/usage.md`
is the reference.

### UI skeleton

Atomic design under `templates/django_fundamentals/`
(`atoms/` → `molecules/` → `organisms/` → `layouts/`). Key invariants:

- **Token mapping lives in the package** (`static/django_fundamentals/tailwind-preset.js`),
  **token values live in the host project** (`static/src/tokens.css`). Colours
  are space-separated RGB channels so Tailwind opacity modifiers work.
- The preset registers form-control styling as **element-level base styles**,
  not utility classes, so allauth pages this package never templated still get
  styled inputs. It also avoids `require("tailwindcss/plugin")` — the file is
  loaded from site-packages, where there is no `node_modules` above it.
- allauth is themed through its **three layouts + its `elements/*` templates**,
  not per-page overrides. `account/verification_sent.html` is the single page
  template overridden. Adding per-page allauth overrides is a regression —
  it breaks the "all ~30 pages themed for free" property.
- `500.html` is intentionally standalone: no `{% extends %}`, no `{% static %}`,
  no `request`, CSS inlined, because whatever caused the 500 may be the database
  or the staticfiles backend.
- Template tags (`templatetags/django_fundamentals.py`): `button_classes`,
  `is_active`, `nav_url`. `nav_url` swallows `NoReverseMatch` on purpose — nav
  is settings-driven, so a bad entry must degrade to a dead link, not a 500.

`docs/source/ui.md` documents tokens, layouts, components and blocks; keep it in
sync when changing any of them.

### DEBUG-only signup affordance

`adapters.AccountAdapter` stashes the email-confirmation URL in the session and
`context_processors.design` surfaces it to `verification_sent.html`, so signup
can be completed locally without SMTP. Both sides are gated on
`settings.DEBUG`; outside DEBUG it would let anyone verify someone else's
address. Keep the gate on both.

## Git workflow — strict Gitflow

`main` and `develop` are long-lived. **Never commit to either directly** — a
`pre-commit` hook rejects commits on `main` outright ("Direct commits to main
are not allowed"), and `develop` is off-limits by convention.

| Branch | Base | Merges into |
|---|---|---|
| `feature/<slug>` | `develop` | `develop` |
| `release/<version>` | `develop` | `main` **and** `develop` |
| `hotfix/<slug>` | `main` | `main` **and** `develop` |

Gitflow has no `docs/` or `chore/` branch type — documentation and maintenance
work is a `feature/*` unless it is a production hotfix.

**Propose the branch name to the user and wait for approval before creating
it.** Do not auto-name and auto-create.

`main` is the release lineage: a `v*` tag on `main` publishes to PyPI, so it
only ever receives reviewed merges from `release/*` or `hotfix/*`.

## Conventions

- **Local variables and function arguments are camelCase** (`targetObject`,
  `resolvedUrls`, `newSuperuser`, fixtures like `regularUser`/`staffUser`).
  Django/DRF API surfaces keep their required snake_case names. Match the
  surrounding style rather than PEP 8 defaults.
- **Comments are UPPERCASE and explain *why*, not what** — usually a trap that
  was hit once. They are load-bearing documentation; do not tidy them into
  sentence case or delete them as noise.
- Docstrings: an italic one-line summary (`"""*does the thing*"""`), then
  `**Key Arguments:**`, `**Return:**`, `**Usage:**` sections with fenced code
  blocks, matching the Sphinx/MyST docs.
- `MANIFEST.in` starts with `recursive-exclude * *`, so any new non-`.py` asset
  directory must be explicitly re-included or it vanishes from the sdist.
- Commits are conventional (`feat:`, `fix:`, `docs:`, `chore:`). Every
  user-visible change gets a `CHANGES.md` entry tagged
  **FEATURE**/**FIXED**/**ENHANCEMENT**/**REFACTOR**/**DOCS**.

## Testing

- Fixtures in `tests/conftest.py`: `regularUser`, `otherUser`, `staffUser`,
  `superUser`. `tests/testapp/` provides a `Note` model (owner + TimeStampedModel)
  for exercising ownership permissions.
- UI tests assert on `THEMED_MARKER = b"text-ink"` rather than just a 200 —
  a 200 alone passes for a completely unstyled allauth fallback page. Keep that
  assertion when adding page tests.
- The suite is the only way this package is run; if a change can't be observed
  through `tests/settings.py`, it isn't covered.

## Modules

@~/.claude/modules/code/python/code_python_django_fundamentals.md
