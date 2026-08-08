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
    assert b"Log in" in response.content


def test_signup_page_renders(client):
    response = client.get(reverse("account_signup"))
    assert response.status_code == 200
    assert b"Sign up" in response.content


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
