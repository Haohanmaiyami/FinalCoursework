import datetime as dt
import pytest
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from habits.models import Habit

User = get_user_model()


@pytest.fixture
def api():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="u1", password="pass12345")


@pytest.fixture
def token(api, user):
    resp = api.post(
        reverse("login"), {"username": "u1", "password": "pass12345"}, format="json"
    )
    assert resp.status_code == 200
    return resp.data["access"]


@pytest.fixture
def auth(api, token):
    api.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")
    return api


def test_register(db, api):
    r = api.post(
        reverse("register"),
        {"username": "new", "email": "e@e.com", "password": "pass12345"},
        format="json",
    )
    assert r.status_code == 201


def test_create_habit_reward_and_linked_forbidden(db, auth, user):
    pleasant = Habit.objects.create(
        user=user,
        place="home",
        time=dt.time(9, 0),
        action="coffee",
        is_pleasant=True,
        period=1,
        length=60,
    )
    data = {
        "place": "street",
        "time": "08:00:00",
        "action": "run",
        "is_pleasant": False,
        "linked": pleasant.id,
        "period": 1,
        "reward": "cake",
        "length": 60,
    }
    assert auth.post("/habit/", data, format="json").status_code == 400


def test_length_limit(db, auth):
    data = {
        "place": "gym",
        "time": "07:00:00",
        "action": "stretch",
        "is_pleasant": False,
        "period": 1,
        "length": 130,
    }
    assert auth.post("/habit/", data, format="json").status_code == 400


def test_linked_must_be_pleasant(db, auth, user):
    not_pl = Habit.objects.create(
        user=user,
        place="park",
        time=dt.time(10, 0),
        action="walk",
        is_pleasant=False,
        period=1,
        length=60,
    )
    data = {
        "place": "home",
        "time": "11:00:00",
        "action": "read",
        "is_pleasant": False,
        "linked": not_pl.id,
        "period": 1,
        "length": 60,
    }
    assert auth.post("/habit/", data, format="json").status_code == 400


def test_pleasant_no_reward_no_linked(db, auth):
    data = {
        "place": "home",
        "time": "09:00:00",
        "action": "bath",
        "is_pleasant": True,
        "period": 1,
        "length": 60,
        "reward": "cake",
    }
    assert auth.post("/habit/", data, format="json").status_code == 400


def test_period_max_7(db, auth):
    data = {
        "place": "home",
        "time": "09:00:00",
        "action": "meditate",
        "is_pleasant": False,
        "period": 8,
        "length": 60,
    }
    assert auth.post("/habit/", data, format="json").status_code == 400


def test_list_only_own_and_pagination(db, auth, user):
    for i in range(7):
        Habit.objects.create(
            user=user,
            place=f"p{i}",
            time=dt.time(9, 0),
            action=f"a{i}",
            is_pleasant=False,
            period=1,
            length=60,
        )
    r1 = auth.get("/habit/?page=1")
    r2 = auth.get("/habit/?page=2")
    assert r1.status_code == 200 and r2.status_code == 200
    assert len(r1.data["results"]) == 5
    assert len(r2.data["results"]) == 2


def test_public_list_without_auth_and_without_pagination(db, api, user):
    Habit.objects.create(
        user=user,
        place="p",
        time=dt.time(9, 0),
        action="a",
        is_pleasant=False,
        period=1,
        length=60,
        is_public=True,
    )
    r = api.get("/habit/public/")
    assert r.status_code == 200
    assert isinstance(r.data, list) and len(r.data) == 1


def test_permissions_owner_only_update(db, user, api):
    # создаём второго
    # логинимся вторым
    resp = api.post(
        reverse("login"), {"username": "u2", "password": "pass12345"}, format="json"
    )
    api.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.data['access']}")
    # чужая привычка
    h = Habit.objects.create(
        user=user,
        place="p",
        time=dt.time(9, 0),
        action="a",
        is_pleasant=False,
        period=1,
        length=60,
    )
    r = api.patch(f"/habit/{h.id}/", {"action": "hack"}, format="json")
    assert r.status_code in (403, 404)


# добавь в tests.py
def test_permissions_read_public_and_owner_write(db, api):
    from django.contrib.auth import get_user_model
    from habits.models import Habit
    from django.urls import reverse

    User = get_user_model()

    owner = User.objects.create_user(username="own", password="pass")

    # публичную может читать аноним
    h_pub = Habit.objects.create(
        user=owner,
        place="p",
        time=dt.time(9, 0),
        action="a",
        is_pleasant=False,
        period=1,
        length=60,
        is_public=True,
    )
    r = api.get(f"/habit/{h_pub.id}/")
    assert r.status_code == 200

    # владелец может править
    resp = api.post(
        reverse("login"), {"username": "own", "password": "pass"}, format="json"
    )
    api.credentials(HTTP_AUTHORIZATION=f"Bearer {resp.data['access']}")
    r = api.patch(f"/habit/{h_pub.id}/", {"action": "edit"}, format="json")
    assert r.status_code in (200, 204)

    # другой пользователь не может править приватную
    h_priv = Habit.objects.create(
        user=owner,
        place="p2",
        time=dt.time(10, 0),
        action="b",
        is_pleasant=False,
        period=1,
        length=60,
        is_public=False,
    )
    resp2 = api.post(
        reverse("login"), {"username": "oth", "password": "pass"}, format="json"
    )
    api.credentials(HTTP_AUTHORIZATION=f"Bearer {resp2.data['access']}")
    r = api.patch(f"/habit/{h_priv.id}/", {"action": "hack"}, format="json")
    assert r.status_code in (403, 404)
