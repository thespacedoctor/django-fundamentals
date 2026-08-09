"""*allauth adapters*"""

from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

# SESSION KEY UNDER WHICH THE MOST RECENT CONFIRMATION URL IS STASHED IN DEBUG.
DEV_CONFIRMATION_URL_SESSION_KEY = "df_dev_confirmation_url"


class AccountAdapter(DefaultAccountAdapter):
    """*default account adapter, plus a development-only convenience*

    With ``ACCOUNT_EMAIL_VERIFICATION = "mandatory"`` and no SMTP server
    configured locally, the confirmation link exists only in the console log.
    In ``DEBUG`` this adapter also stashes it in the session so
    ``account/verification_sent.html`` can show it directly, letting a
    developer finish signing up without leaving the browser.

    Never active outside ``DEBUG``, where exposing the link would let anyone
    verify someone else's address.
    """

    def get_email_confirmation_url(self, request, emailconfirmation):
        """*build the confirmation URL, stashing it in the session when DEBUG*

        **Key Arguments:**

        - ``request`` -- the current request
        - ``emailconfirmation`` -- the allauth ``EmailConfirmation`` instance

        **Return:**

        - ``confirmationUrl`` -- the absolute confirmation URL
        """
        confirmationUrl = super().get_email_confirmation_url(request, emailconfirmation)

        if settings.DEBUG and request is not None and hasattr(request, "session"):
            request.session[DEV_CONFIRMATION_URL_SESSION_KEY] = confirmationUrl

        return confirmationUrl
