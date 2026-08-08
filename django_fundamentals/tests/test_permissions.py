import pytest
from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory

from django_fundamentals.permissions import (
    IsOwnerOrReadOnly,
    IsStaffUser,
    IsSuperUser,
    assign_owner_permissions,
)

pytestmark = pytest.mark.django_db


def test_anonymous_user_is_read_only_tier():
    assert AnonymousUser().is_authenticated is False


def test_is_owner_or_read_only_allows_owner_write(regularUser):
    from django_fundamentals.tests.testapp.models import Note

    note = Note.objects.create(owner=regularUser, title="mine")
    request = RequestFactory().post("/")
    request.user = regularUser

    assert IsOwnerOrReadOnly().has_object_permission(request, None, note) is True


def test_is_owner_or_read_only_blocks_non_owner_write(regularUser, otherUser):
    from django_fundamentals.tests.testapp.models import Note

    note = Note.objects.create(owner=regularUser, title="mine")
    request = RequestFactory().post("/")
    request.user = otherUser

    assert IsOwnerOrReadOnly().has_object_permission(request, None, note) is False


def test_is_owner_or_read_only_allows_read_for_anyone(regularUser, otherUser):
    from django_fundamentals.tests.testapp.models import Note

    note = Note.objects.create(owner=regularUser, title="mine")
    request = RequestFactory().get("/")
    request.user = otherUser

    assert IsOwnerOrReadOnly().has_object_permission(request, None, note) is True


def test_is_staff_user_permission(staffUser, regularUser):
    request = RequestFactory().get("/")

    request.user = staffUser
    assert IsStaffUser().has_permission(request, None) is True

    request.user = regularUser
    assert IsStaffUser().has_permission(request, None) is False


def test_is_super_user_permission(superUser, staffUser):
    request = RequestFactory().get("/")

    request.user = superUser
    assert IsSuperUser().has_permission(request, None) is True

    request.user = staffUser
    assert IsSuperUser().has_permission(request, None) is False


def test_assign_owner_permissions_grants_guardian_object_perms(regularUser):
    from django_fundamentals.tests.testapp.models import Note

    note = Note.objects.create(owner=regularUser, title="mine")
    assign_owner_permissions(regularUser, note)

    assert regularUser.has_perm("view_note", note)
    assert regularUser.has_perm("change_note", note)
    assert regularUser.has_perm("delete_note", note)
