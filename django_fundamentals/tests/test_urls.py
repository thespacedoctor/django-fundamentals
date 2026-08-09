import pytest
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_account_login_url_resolves():
    assert reverse("account_login") == "/accounts/login/"


def test_account_signup_url_resolves():
    assert reverse("account_signup") == "/accounts/signup/"


def test_login_page_renders(client):
    response = client.get(reverse("account_login"))
    assert response.status_code == 200
    # allauth's OWN COPY — WE NO LONGER SHIP A HAND-ROLLED login.html, SO THAT
    # ITS SOCIAL/PASSKEY/LOGIN-BY-CODE FEATURES KEEP WORKING.
    assert b"Sign In" in response.content
    # AND IT MUST COME THROUGH OUR THEMED ELEMENTS, NOT allauth's BARE DEFAULTS.
    assert b"text-ink" in response.content


def test_signup_page_renders(client):
    response = client.get(reverse("account_signup"))
    assert response.status_code == 200
    assert b"Sign Up" in response.content
    assert b"text-ink" in response.content


def test_rest_auth_registration_endpoint_exists(client):
    response = client.post("/api/auth/registration/", {})
    # A 400 (validation error) proves the endpoint is wired up and reachable,
    # as opposed to a 404 which would mean the include() is broken.
    assert response.status_code == 400


def test_home_url_resolves_to_root():
    assert reverse("django_fundamentals_home") == "/"


def test_homepage_renders_with_known_urls(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"/accounts/login/" in response.content
    assert b"/api/auth/registration/" in response.content


def test_login_redirects_to_homepage_not_a_404(client, regularUser):
    from allauth.account.models import EmailAddress

    EmailAddress.objects.create(
        user=regularUser, email=regularUser.email, verified=True, primary=True
    )

    response = client.post(
        reverse("account_login"),
        {"login": regularUser.email, "password": "pw12345!"},
    )
    assert response.status_code == 302
    assert response.url == "/"

    followed = client.get(response.url)
    assert followed.status_code == 200


def test_account_email_verification_sent_uses_allauths_own_view(client, regularUser):
    # dj_rest_auth.registration.urls ALSO REGISTERS THIS NAME AS AN EMPTY
    # PLACEHOLDER TemplateView; IF THAT ONE EVER SHADOWS allauth's REAL VIEW AGAIN
    # (e.g. A FUTURE INCLUDE-ORDER CHANGE), THIS 500s INSTEAD OF RENDERING.
    response = client.post(
        reverse("account_signup"),
        {
            "username": "gina",
            "email": "gina@example.com",
            "password1": "SuperSecret123!",
            "password2": "SuperSecret123!",
        },
    )
    assert response.status_code == 302

    followed = client.get(response.url)
    assert followed.status_code == 200
