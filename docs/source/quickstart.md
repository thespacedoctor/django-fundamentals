# Quickstart

## Install

Create and activate an isolated conda environment, then install with pip:

```bash
conda create -n django-fundamentals pip -c conda-forge
conda activate django-fundamentals
pip install django-fundamentals
```

## Wire it into a project's settings

```python
from django_fundamentals.settings import (
    ACCOUNT_EMAIL_VERIFICATION,
    ACCOUNT_LOGIN_METHODS,
    ACCOUNT_LOGOUT_REDIRECT_URL,
    ACCOUNT_SIGNUP_FIELDS,
    ACCOUNT_UNIQUE_EMAIL,
    ANONYMOUS_USER_NAME,
    BASE_AUTHENTICATION_BACKENDS,
    BASE_INSTALLED_APPS,
    BASE_MIDDLEWARE,
    BASE_REST_FRAMEWORK,
    BASE_TEMPLATE_CONTEXT_PROCESSORS,
    LOGIN_REDIRECT_URL,
    REST_AUTH,
)

AUTH_USER_MODEL = "django_fundamentals.User"
INSTALLED_APPS = [*BASE_INSTALLED_APPS, "myproject.apps.core"]
MIDDLEWARE = [*BASE_MIDDLEWARE, "myproject.middleware.SomeMiddleware"]
AUTHENTICATION_BACKENDS = BASE_AUTHENTICATION_BACKENDS
REST_FRAMEWORK = BASE_REST_FRAMEWORK
SITE_ID = 1

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "APP_DIRS": True,
        "OPTIONS": {"context_processors": BASE_TEMPLATE_CONTEXT_PROCESSORS},
    }
]
```

The `ACCOUNT_*`, `ANONYMOUS_USER_NAME`, `LOGIN_REDIRECT_URL`, and `REST_AUTH`
imports aren't reassigned to anything — just importing them into your
settings module is enough, since Django picks up any uppercase name present
in that module's namespace as a real setting. **Leaving any of them out
silently falls back to Django/allauth's own defaults** — most notably
`LOGIN_REDIRECT_URL`, which defaults to `/accounts/profile/` and will 404
after every login/signup unless imported (or set to something else) here.

## Wire it into a project's urls.py

```python
from django.urls import include, path

urlpatterns = [
    path("", include("django_fundamentals.urls")),
]
```

This exposes:

- `/accounts/...` — server-rendered allauth login/signup/logout/password-reset.
- `/api/auth/...` — dj-rest-auth DRF endpoints for the same flows.

## Migrate

```bash
python manage.py migrate
```

## Tailwind CSS

The base layout links a project-supplied, compiled stylesheet at
`static/css/tailwind.css`. Building it is the host project's responsibility —
see [django-fundamentals-cookiecutter](https://github.com/thespacedoctor/django-fundamentals-cookiecutter),
which ships a working `tailwind.config.js` / `package.json` pipeline.

Your `tailwind.config.js` **must scan this package's templates as well as your
own**, or every class used by the sidebar, navbar and auth pages is purged and
the app renders unstyled. Don't hard-code a path like `./.venv/lib/**` — under
conda, site-packages lives outside the project entirely. Ask Python where the
package actually is:

```js
const { execSync } = require("child_process");
const packageDir = execSync(
    'python -c "import django_fundamentals,os;print(os.path.dirname(django_fundamentals.__file__))"',
    { encoding: "utf8" }
).trim();

module.exports = {
    presets: [require(path.join(packageDir, "static/django_fundamentals/tailwind-preset.js"))],
    content: ["./templates/**/*.html", path.join(packageDir, "templates/**/*.html")],
};
```

See [UI skeleton](ui.md) for the design tokens this drives.
