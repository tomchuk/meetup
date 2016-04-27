from django.contrib.auth.models import update_last_login
from django.contrib.auth.signals import user_logged_in
from rest_framework.test import APIClient
import pytest

pytestmark = pytest.mark.django_db


class TestClient(APIClient):

    def login(self, user):
        user.backend = 'todo.backends.FacebookBackend'
        user_logged_in.disconnect(update_last_login)
        super(TestClient, self)._login(user)
        return True


@pytest.fixture
def client():
    return TestClient()
