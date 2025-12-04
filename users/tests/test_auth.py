from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
import pytest

User = get_user_model()


@pytest.mark.django_db
def test_login_jwt():
    User.objects.create_user(username="u2", password="pass12345")
    api = APIClient()
    r = api.post(
        reverse("login"), {"username": "u2", "password": "pass12345"}, format="json"
    )
    assert r.status_code == 200 and "access" in r.data
