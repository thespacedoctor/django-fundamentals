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
    BASE_INSTALLED_APPS,
    BASE_MIDDLEWARE,
    BASE_AUTHENTICATION_BACKENDS,
    BASE_REST_FRAMEWORK,
    BASE_TEMPLATE_CONTEXT_PROCESSORS,
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

`django_fundamentals/templates/django_fundamentals/base.html` links a
project-supplied, compiled stylesheet at `static/css/tailwind.css`. Building
that file is the host project's responsibility — see
[django-fundamentals-cookiecutter](https://github.com/thespacedoctor/django-fundamentals-cookiecutter),
which ships a working `tailwind.config.js` / `package.json` build pipeline.
