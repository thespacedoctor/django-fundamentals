# django-fundamentals

A reusable base Django app used as a shared/common foundation for other Django apps. Install it into a project and get, out of
the box:

- A custom `User` model.
- Authentication wired through [django-allauth](https://docs.allauth.org/) + [dj-rest-auth](https://dj-rest-auth.readthedocs.io/) — signup, login, logout, and password reset, both as server-rendered views under `/accounts/` and as DRF endpoints under `/api/auth/` (`/api/auth/registration/`, `/api/auth/login/`, `/api/auth/password/reset/`).
- Object-level permissions via [django-guardian](https://django-guardian.readthedocs.io/), plus a 4-tier authorization model: `Anonymous` / `Authenticated` / `Staff` / `Superuser`.
- DRF `TokenAuthentication` for API clients.
- A server-rendered frontend baseline: Django templates as the source of truth, [HTMX](https://htmx.org/) for server communication, [Alpine.js](https://alpinejs.dev/) for local UI state, and [Tailwind CSS](https://tailwindcss.com/) for styling.
- A complete **UI skeleton** built from atomic-design components: app shell with sidebar and top navbar, a centered layout for auth pages, styled 404/403/400/500 pages, favicons, and dark mode. All colours and dimensions come from one design-token file. Every `django-allauth` page is themed. See `docs/source/ui.md`.

New projects are generated from [django-fundamentals-cookiecutter](https://github.com/thespacedoctor/django-fundamentals-cookiecutter), which pins this package as a dependency. Updates to this package (`pip install -U django-fundamentals`) propagate into every project built on
top of.

## Installation

Create and activate an isolated conda environment, then install with pip:

```bash
conda create -n django-fundamentals pip -c conda-forge
conda activate django-fundamentals
pip install django-fundamentals
```

## Quickstart

In your Django project's `settings.py` (abbreviated — see
`docs/source/quickstart.md` for the full, copy-pasteable version, including
the `ACCOUNT_*`/`LOGIN_REDIRECT_URL`/`REST_AUTH` imports that must also be
present or you'll silently fall back to Django/allauth's own defaults):

```python
from django_fundamentals.settings import BASE_INSTALLED_APPS, BASE_MIDDLEWARE, BASE_AUTHENTICATION_BACKENDS, BASE_REST_FRAMEWORK

AUTH_USER_MODEL = "django_fundamentals.User"
INSTALLED_APPS = [*BASE_INSTALLED_APPS, ...]
MIDDLEWARE = [*BASE_MIDDLEWARE, ...]
AUTHENTICATION_BACKENDS = BASE_AUTHENTICATION_BACKENDS
REST_FRAMEWORK = BASE_REST_FRAMEWORK
SITE_ID = 1
```

In your project's `urls.py`:

```python
from django.urls import include, path

urlpatterns = [
    path("", include("django_fundamentals.urls")),
    ...
]
```

See `docs/source/quickstart.md` for the full setup, including Tailwind/HTMX
static-file wiring and the 4-tier permission helpers.

## Development

```bash
conda create -n django-fundamentals pip -c conda-forge
conda activate django-fundamentals
pip install -e .[dev]
pytest
```

## License

GNU General Public License v3 (or later). See `LICENSE`.
