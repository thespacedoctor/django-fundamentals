from django.core.management.base import BaseCommand

from django_fundamentals.models import User


class Command(BaseCommand):
    """*create a superuser from env vars if no superuser exists yet — safe to run on every deploy*

    **Usage:**

    ```bash
    DJANGO_SUPERUSER_USERNAME=admin \\
    DJANGO_SUPERUSER_EMAIL=admin@example.com \\
    DJANGO_SUPERUSER_PASSWORD=change-me \\
    python manage.py create_superuser_if_none
    ```
    """

    help = "Create a superuser from DJANGO_SUPERUSER_* env vars if none exists yet."

    def handle(self, *args, **options):
        import os

        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write("A superuser already exists, skipping.")
            return

        userName = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        userEmail = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        userPassword = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not (userName and userEmail and userPassword):
            self.stdout.write(
                self.style.WARNING(
                    "DJANGO_SUPERUSER_USERNAME/EMAIL/PASSWORD not all set, skipping."
                )
            )
            return

        newSuperuser = User.objects.create_superuser(
            username=userName, email=userEmail, password=userPassword
        )

        # PRE-VERIFY THE EMAIL SO THE BOOTSTRAP SUPERUSER CAN LOG IN IMMEDIATELY EVEN
        # WHEN ACCOUNT_EMAIL_VERIFICATION IS "mandatory" AND NO SMTP IS SET UP YET
        from allauth.account.models import EmailAddress

        EmailAddress.objects.update_or_create(
            user=newSuperuser,
            email=userEmail,
            defaults={"verified": True, "primary": True},
        )

        self.stdout.write(self.style.SUCCESS(f"Created superuser '{userName}'."))
