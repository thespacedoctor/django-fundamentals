from django.contrib.auth.models import AbstractUser
from django.db import models

from django_fundamentals.managers import UserManager
from django_fundamentals.storage import AvatarStorage


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

    # SERVED BY django_fundamentals.views.AvatarView, NOT BY THE WEB SERVER —
    # SEE THAT VIEW FOR WHY THERE IS NO MEDIA_URL TO CONFIGURE.
    avatar = models.ImageField(
        upload_to="avatars/",
        storage=AvatarStorage(),
        blank=True,
        help_text="Square images work best. Leave empty to use your initials.",
    )

    objects = UserManager()

    class Meta:
        app_label = "django_fundamentals"

    @property
    def display_name(self):
        """*the friendliest name available for this user*

        **Return:**

        - ``displayName`` -- full name if set, otherwise the username

        **Usage:**

        ```django
        {{ request.user.display_name }}
        ```
        """
        return self.get_full_name() or self.get_username()

    def get_initials(self):
        """*one or two letters standing in for a missing profile picture*

        Falls back through full name, then username, then email, so every
        user renders something — a blank avatar tile would look broken.

        **Return:**

        - ``initials`` -- an uppercase one or two character string

        **Usage:**

        ```django
        {{ user.get_initials }}
        ```
        """
        firstName = (self.first_name or "").strip()
        lastName = (self.last_name or "").strip()
        if firstName and lastName:
            return f"{firstName[0]}{lastName[0]}".upper()

        # A SINGLE NAME, A USERNAME, OR AN EMAIL — WHICHEVER TURNS UP FIRST
        for candidate in (firstName, lastName, self.get_username(), self.email):
            candidate = (candidate or "").strip()
            if candidate:
                return candidate[0].upper()

        return "?"
