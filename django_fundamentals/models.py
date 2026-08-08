from django.contrib.auth.models import AbstractUser
from django.db import models

from django_fundamentals.managers import UserManager


class TimeStampedModel(models.Model):
    """*abstract base model adding created/updated timestamps*

    **Usage:**

    ```python
    class Widget(TimeStampedModel):
        name = models.CharField(max_length=200)
    ```
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser):
    """*custom user model, the target of ``AUTH_USER_MODEL``*

    Subclasses ``AbstractUser`` rather than adding fields to it directly, so
    downstream projects can extend this model further without a migration
    conflict inside this package.

    **Usage:**

    ```python
    # settings.py
    AUTH_USER_MODEL = "django_fundamentals.User"
    ```
    """

    objects = UserManager()

    class Meta:
        app_label = "django_fundamentals"
