"""*tests for username collection at signup and username-or-email login*"""

import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

pytestmark = pytest.mark.django_db


def test_signup_collects_a_username(client):
    response = client.post(
        reverse("account_signup"),
        {
            "username": "newcomer",
            "email": "newcomer@example.com",
            "password1": "sup3rsecret!pw",
            "password2": "sup3rsecret!pw",
        },
    )
    assert response.status_code == 302

    newUser = get_user_model().objects.get(email="newcomer@example.com")
    # THE POINT OF COLLECTING IT: THE USERNAME IS WHAT THEY CHOSE, NOT SOMETHING
    # allauth's populate_username() DERIVED FROM THE EMAIL.
    assert newUser.username == "newcomer"


def test_signup_rejects_a_missing_username(client):
    response = client.post(
        reverse("account_signup"),
        {
            "email": "nameless@example.com",
            "password1": "sup3rsecret!pw",
            "password2": "sup3rsecret!pw",
        },
    )
    assert response.status_code == 200
    assert not get_user_model().objects.filter(email="nameless@example.com").exists()


def test_signup_form_renders_a_username_field(client):
    response = client.get(reverse("account_signup"))
    assert b'name="username"' in response.content


@pytest.mark.parametrize("identifier", ["username", "email"])
def test_login_accepts_either_identifier(client, regularUser, identifier):
    from allauth.account.models import EmailAddress

    # ACCOUNT_EMAIL_VERIFICATION IS "mandatory", SO AN UNVERIFIED USER IS SENT
    # TO THE CONFIRM-EMAIL PAGE NO MATTER WHICH IDENTIFIER THEY USED.
    EmailAddress.objects.create(
        user=regularUser, email=regularUser.email, verified=True, primary=True
    )

    credential = (
        regularUser.username if identifier == "username" else regularUser.email
    )
    response = client.post(
        reverse("account_login"),
        {"login": credential, "password": "pw12345!"},
    )
    assert response.status_code == 302
    assert response.wsgi_request.user.is_authenticated
