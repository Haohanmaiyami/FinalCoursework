def test_send_habit_reminders_sends_message(monkeypatch, db, settings):
    # делаем время на ближайшую минуту
    from django.utils import timezone

    now = timezone.localtime()
    minute = now.replace(second=0, microsecond=0).time()

    # пользователь с chat_id
    from django.contrib.auth import get_user_model

    User = get_user_model()
    u = User.objects.create_user(username="tguser", password="pass12345")
    u.tg_chat_id = 470794575
    u.save()

    # полезная привычка ровно на эту минуту
    from habits.models import Habit

    Habit.objects.create(
        user=u,
        place="дом",
        time=minute,
        action="читать",
        is_pleasant=False,
        period=1,
        length=60,
        is_public=False,
    )

    # в TG
    calls = {"n": 0}

    def fake_send(chat_id, text):
        calls["n"] += 1
        assert str(chat_id).isdigit()
        assert "Напоминание" in text

    monkeypatch.setattr("tg.tasks.send_telegram_message", fake_send)

    # вызываем таску напрямую (без celery worker)
    from tg.tasks import send_habit_reminders

    send_habit_reminders()
    assert calls["n"] >= 1
