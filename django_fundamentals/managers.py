from django.contrib.auth.models import UserManager as DjangoUserManager


class UserManager(DjangoUserManager):
    """Default Django UserManager, kept as an explicit subclass so
    downstream projects have a stable hook to extend without touching this
    package."""
