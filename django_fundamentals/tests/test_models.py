import pytest

pytestmark = pytest.mark.django_db


def test_user_is_active_by_default(regularUser):
    assert regularUser.is_active is True
    assert regularUser.is_staff is False
    assert regularUser.is_superuser is False


def test_staff_user_flags(staffUser):
    assert staffUser.is_staff is True
    assert staffUser.is_superuser is False


def test_superuser_flags(superUser):
    assert superUser.is_staff is True
    assert superUser.is_superuser is True


def test_timestamped_model_sets_created_and_updated_at(regularUser):
    from django_fundamentals.tests.testapp.models import Note

    note = Note.objects.create(owner=regularUser, title="hello")
    assert note.created_at is not None
    assert note.updated_at is not None
