"""*tests for the UI skeleton: layouts, components, theming and status pages*"""

import pytest
from django.template.loader import render_to_string
from django.test import RequestFactory
from django.urls import reverse

from django_fundamentals.context_processors import DEFAULT_SIDEBAR_NAV, design
from django_fundamentals.templatetags.django_fundamentals import (
    button_classes,
    is_active,
    nav_url,
)

pytestmark = pytest.mark.django_db

# A CLASS ONLY THE TOKEN-DRIVEN SKELETON EMITS. ASSERTING ON IT PROVES A PAGE
# CAME THROUGH OUR LAYOUTS RATHER THAN A BARE allauth/DJANGO FALLBACK — A 200
# ALONE WOULD PASS EVEN FOR A COMPLETELY UNSTYLED PAGE.
THEMED_MARKER = b"text-ink"


# --- template tags ---------------------------------------------------------


def test_button_classes_defaults_to_primary():
    assert "bg-brand" in button_classes()


def test_button_classes_honours_variant():
    assert "bg-danger" in button_classes(variant="danger")
    assert "border-line" in button_classes(variant="secondary")


def test_button_classes_unknown_variant_falls_back_to_primary():
    assert "bg-brand" in button_classes(variant="not-a-variant")


def test_button_classes_full_width():
    assert " w-full" in button_classes(full=True)
    assert " w-full" not in button_classes(full=False)


def test_nav_url_reverses_known_name():
    assert nav_url("account_login") == "/accounts/login/"


def test_nav_url_returns_empty_for_unknown_name():
    # SIDEBAR ENTRIES COME FROM SETTINGS, SO A TYPO MUST DEGRADE TO A DEAD LINK
    # RATHER THAN 500 EVERY PAGE THAT RENDERS THE SIDEBAR.
    assert nav_url("no_such_url_name") == ""


def test_is_active_matches_current_view():
    request = RequestFactory().get("/")
    request.resolver_match = type("M", (), {"url_name": "django_fundamentals_home"})()
    assert is_active({"request": request}, "django_fundamentals_home") is True
    assert is_active({"request": request}, "account_login") is False


def test_is_active_without_request_is_false():
    assert is_active({}, "django_fundamentals_home") is False


# --- context processor -----------------------------------------------------


def test_design_context_supplies_chrome_defaults():
    context = design(RequestFactory().get("/"))
    assert context["df_site_name"]
    assert context["df_sidebar_nav"] == DEFAULT_SIDEBAR_NAV
    assert context["df_version"]


def test_design_context_respects_settings_overrides(settings):
    settings.DJANGO_FUNDAMENTALS_SITE_NAME = "Acme"
    settings.DJANGO_FUNDAMENTALS_SIDEBAR_NAV = [{"label": "X", "url_name": "y"}]
    context = design(RequestFactory().get("/"))
    assert context["df_site_name"] == "Acme"
    assert context["df_sidebar_nav"] == [{"label": "X", "url_name": "y"}]


# --- layouts ---------------------------------------------------------------


def test_homepage_uses_app_shell(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Sidebar navigation" in response.content
    assert THEMED_MARKER in response.content


def test_auth_pages_use_centered_layout_not_app_shell(client):
    response = client.get(reverse("account_login"))
    assert response.status_code == 200
    assert THEMED_MARKER in response.content
    # NO SIDEBAR BEFORE A VISITOR HAS SIGNED IN
    assert b"Sidebar navigation" not in response.content


def test_base_layout_emits_no_flash_theme_boot(client):
    # THE THEME MUST BE APPLIED BY A SYNCHRONOUS INLINE SCRIPT IN <head>;
    # WAITING FOR ALPINE WOULD FLASH THE LIGHT THEME FIRST.
    content = client.get("/").content
    assert b"prefers-color-scheme" in content
    assert content.index(b"prefers-color-scheme") < content.index(b"<body")


def test_favicons_and_manifest_are_linked(client):
    content = client.get("/").content
    for asset in (b"favicon.svg", b"favicon.ico", b"apple-touch-icon.png", b"site.webmanifest"):
        assert asset in content


# --- allauth theming -------------------------------------------------------


@pytest.mark.parametrize(
    "urlName",
    ["account_login", "account_signup", "account_reset_password"],
)
def test_anonymous_allauth_pages_are_themed(client, urlName):
    response = client.get(reverse(urlName))
    assert response.status_code == 200
    assert THEMED_MARKER in response.content


@pytest.mark.parametrize("urlName", ["account_email", "account_change_password"])
def test_authenticated_allauth_pages_are_themed(client, regularUser, urlName):
    client.force_login(regularUser)
    response = client.get(reverse(urlName))
    assert response.status_code == 200
    assert THEMED_MARKER in response.content


def test_allauth_layouts_are_overridden_by_this_package():
    # allauth's OWN base LAYOUT IS AN UNSTYLED BARE-HTML PAGE. IF OUR OVERRIDE
    # EVER STOPS WINNING THE TEMPLATE-LOADER RACE (e.g. INSTALLED_APPS ORDER
    # CHANGES), EVERY allauth PAGE SILENTLY LOSES ITS STYLING.
    for layout in ("base", "entrance", "manage"):
        rendered = render_to_string(f"allauth/layouts/{layout}.html")
        assert "Menu:" not in rendered, f"{layout} fell through to allauth's own layout"


# --- status pages ----------------------------------------------------------


def test_404_template_is_themed():
    rendered = render_to_string("404.html")
    assert "Page not found" in rendered
    assert "text-ink" in rendered


def test_500_template_is_self_contained():
    # RENDERED WITH AN EMPTY CONTEXT BY DJANGO, POSSIBLY WHILE THE DATABASE OR
    # STATICFILES BACKEND IS THE THING THAT BROKE — SO IT MUST NOT INHERIT, USE
    # {% static %}, OR TOUCH `request`.
    rendered = render_to_string("500.html")
    assert "Something went wrong" in rendered
    assert "<style>" in rendered
    assert "/static/" not in rendered

    import pathlib
    import re

    import django_fundamentals

    source = (
        pathlib.Path(django_fundamentals.__file__)
        .parent.joinpath("templates/500.html")
        .read_text()
    )
    # STRIP {# ... #} COMMENTS FIRST — THEY DISCUSS THESE VERY TAGS BY NAME.
    source = re.sub(r"\{#.*?#\}", "", source, flags=re.S)
    assert "{% extends" not in source
    assert "{% static" not in source
    assert "{% include" not in source
