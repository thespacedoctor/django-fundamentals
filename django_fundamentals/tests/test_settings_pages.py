"""*tests for the user settings pages: profile, avatars and the API token*"""

import io

import pytest
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from rest_framework.authtoken.models import Token

pytestmark = pytest.mark.django_db

# SAME MARKER THE REST OF THE UI SUITE USES — A 200 ALONE WOULD PASS FOR AN
# UNSTYLED FALLBACK PAGE.
THEMED_MARKER = b"text-ink"

# A CLASS ONLY organisms/settings_tabs.html EMITS, USED TO PROVE THE TAB RAIL
# REACHED A PAGE THIS PACKAGE NEVER TEMPLATED.
TAB_RAIL_MARKER = b'aria-label="Settings sections"'


def make_png_upload(name="avatar.png"):
    """*build the smallest valid PNG Django's ImageField will accept*

    **Key Arguments:**

    - ``name`` -- the uploaded filename

    **Return:**

    - ``upload`` -- a ``SimpleUploadedFile`` holding a 1x1 PNG

    **Usage:**

    ```python
    client.post(url, {"avatar": make_png_upload()})
    ```
    """
    from PIL import Image

    buffer = io.BytesIO()
    Image.new("RGB", (1, 1), color="red").save(buffer, format="PNG")
    return SimpleUploadedFile(name, buffer.getvalue(), content_type="image/png")


# --- access control --------------------------------------------------------


@pytest.mark.parametrize(
    "urlName",
    ["django_fundamentals_settings", "django_fundamentals_settings_api"],
)
def test_settings_pages_require_login(client, urlName):
    response = client.get(reverse(urlName))
    assert response.status_code == 302
    assert "login" in response["Location"]


@pytest.mark.parametrize(
    "urlName,heading",
    [
        ("django_fundamentals_settings", b"Profile picture"),
        ("django_fundamentals_settings_api", b"Your API token"),
    ],
)
def test_settings_pages_are_themed_and_render_their_own_body(
    client, regularUser, urlName, heading
):
    """Asserting on the page's own content as well as the theme marker: the
    layout chrome alone satisfies THEMED_MARKER, so a settings layout that
    swallowed the content block entirely would still pass without this."""
    client.force_login(regularUser)
    response = client.get(reverse(urlName))
    assert response.status_code == 200
    assert THEMED_MARKER in response.content
    assert heading in response.content


def test_settings_index_redirects_to_profile(client, regularUser):
    client.force_login(regularUser)
    response = client.get(reverse("django_fundamentals_settings_index"))
    assert response.status_code == 302
    assert response["Location"] == reverse("django_fundamentals_settings")


# --- the tab rail ----------------------------------------------------------


def test_tab_rail_renders_on_our_own_settings_page(client, regularUser):
    client.force_login(regularUser)
    response = client.get(reverse("django_fundamentals_settings"))
    assert TAB_RAIL_MARKER in response.content


@pytest.mark.parametrize(
    "urlName,ownContent",
    [
        ("account_email", b"Add Email Address"),
        ("account_change_password", b"<form"),
    ],
)
def test_tab_rail_reaches_allauths_own_pages(client, regularUser, urlName, ownContent):
    """The content_outer mechanism is what puts the rail on pages this package
    never templated. Two ways it can break: the rail stops appearing, or the
    wrapper swallows allauth's own content block. Assert both."""
    client.force_login(regularUser)
    response = client.get(reverse(urlName))
    assert response.status_code == 200
    assert TAB_RAIL_MARKER in response.content
    assert ownContent in response.content


def test_tab_rail_absent_from_ordinary_pages(client, regularUser):
    client.force_login(regularUser)
    response = client.get(reverse("django_fundamentals_home"))
    assert TAB_RAIL_MARKER not in response.content


# --- profile ---------------------------------------------------------------


def test_profile_form_updates_names_and_username(client, regularUser):
    client.force_login(regularUser)
    response = client.post(
        reverse("django_fundamentals_settings"),
        {"username": "alice2", "first_name": "Alice", "last_name": "Adams"},
    )
    assert response.status_code == 302

    regularUser.refresh_from_db()
    assert regularUser.username == "alice2"
    assert regularUser.first_name == "Alice"
    assert regularUser.last_name == "Adams"


def test_profile_form_rejects_a_username_already_taken(client, regularUser, otherUser):
    client.force_login(regularUser)
    response = client.post(
        reverse("django_fundamentals_settings"),
        {"username": otherUser.username, "first_name": "", "last_name": ""},
    )
    assert response.status_code == 200

    regularUser.refresh_from_db()
    assert regularUser.username != otherUser.username


def test_profile_form_accepts_an_avatar_upload(client, regularUser):
    client.force_login(regularUser)
    response = client.post(
        reverse("django_fundamentals_settings"),
        {
            "username": regularUser.username,
            "first_name": "",
            "last_name": "",
            "avatar": make_png_upload(),
        },
    )
    assert response.status_code == 302

    regularUser.refresh_from_db()
    assert regularUser.avatar
    assert "avatars/" in regularUser.avatar.name


# --- avatars ---------------------------------------------------------------


def test_avatar_view_serves_an_uploaded_image(client, regularUser):
    regularUser.avatar = make_png_upload()
    regularUser.save()

    client.force_login(regularUser)
    response = client.get(
        reverse("django_fundamentals_avatar", args=[regularUser.pk])
    )
    assert response.status_code == 200
    assert b"".join(response.streaming_content).startswith(b"\x89PNG")


def test_avatar_view_404s_when_the_user_has_no_avatar(client, regularUser):
    client.force_login(regularUser)
    response = client.get(
        reverse("django_fundamentals_avatar", args=[regularUser.pk])
    )
    assert response.status_code == 404


def test_avatar_view_requires_login(client, regularUser):
    response = client.get(
        reverse("django_fundamentals_avatar", args=[regularUser.pk])
    )
    assert response.status_code == 302


def test_navbar_falls_back_to_initials_without_an_avatar(client, regularUser):
    regularUser.first_name = "Alice"
    regularUser.last_name = "Adams"
    regularUser.save()

    client.force_login(regularUser)
    response = client.get(reverse("django_fundamentals_home"))
    assert b">AA<" in response.content


def test_navbar_uses_the_avatar_image_when_one_exists(client, regularUser):
    regularUser.avatar = make_png_upload()
    regularUser.save()

    client.force_login(regularUser)
    response = client.get(reverse("django_fundamentals_home"))
    avatarUrl = reverse("django_fundamentals_avatar", args=[regularUser.pk])
    assert avatarUrl.encode() in response.content


@pytest.mark.parametrize(
    "firstName,lastName,username,email,expected",
    [
        ("Alice", "Adams", "alice", "a@example.com", "AA"),
        ("Alice", "", "alice", "a@example.com", "A"),
        ("", "", "zebra", "a@example.com", "Z"),
    ],
)
def test_get_initials(db, firstName, lastName, username, email, expected):
    targetUser = get_user_model()(
        first_name=firstName, last_name=lastName, username=username, email=email
    )
    assert targetUser.get_initials() == expected


def test_get_initials_falls_back_to_email_without_a_username(db):
    targetUser = get_user_model()(username="", email="zoe@example.com")
    assert targetUser.get_initials() == "Z"


# --- API token -------------------------------------------------------------


def test_api_tab_shows_the_current_token(client, regularUser):
    apiToken = Token.objects.create(user=regularUser)
    client.force_login(regularUser)
    response = client.get(reverse("django_fundamentals_settings_api"))
    assert apiToken.key.encode() in response.content


def test_api_tab_creates_a_token_for_a_user_who_has_none(client, regularUser):
    assert not Token.objects.filter(user=regularUser).exists()

    client.force_login(regularUser)
    response = client.get(reverse("django_fundamentals_settings_api"))
    assert response.status_code == 200
    assert Token.objects.filter(user=regularUser).exists()


def test_regenerate_replaces_the_token(client, regularUser):
    originalKey = Token.objects.create(user=regularUser).key

    client.force_login(regularUser)
    response = client.post(reverse("django_fundamentals_token_regenerate"))
    assert response.status_code == 302

    assert Token.objects.filter(user=regularUser).count() == 1
    assert Token.objects.get(user=regularUser).key != originalKey


def test_regenerate_rejects_get(client, regularUser):
    originalKey = Token.objects.create(user=regularUser).key

    client.force_login(regularUser)
    response = client.get(reverse("django_fundamentals_token_regenerate"))
    assert response.status_code == 405
    assert Token.objects.get(user=regularUser).key == originalKey


def test_regenerate_requires_login(client):
    response = client.post(reverse("django_fundamentals_token_regenerate"))
    assert response.status_code == 302
