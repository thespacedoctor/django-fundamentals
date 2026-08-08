import pytest
from django.contrib.auth import get_user_model


@pytest.fixture
def regularUser(db):
    UserModel = get_user_model()
    return UserModel.objects.create_user(
        username="alice", email="alice@example.com", password="pw12345!"
    )


@pytest.fixture
def otherUser(db):
    UserModel = get_user_model()
    return UserModel.objects.create_user(
        username="bob", email="bob@example.com", password="pw12345!"
    )


@pytest.fixture
def staffUser(db):
    UserModel = get_user_model()
    return UserModel.objects.create_user(
        username="staffer", email="staff@example.com", password="pw12345!", is_staff=True
    )


@pytest.fixture
def superUser(db):
    UserModel = get_user_model()
    return UserModel.objects.create_superuser(
        username="root", email="root@example.com", password="pw12345!"
    )
