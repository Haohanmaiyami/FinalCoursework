import logging
import datetime as dt
from celery import shared_task
from django.utils import timezone
from django.core.cache import cache

from habits.models import Habit
from .services import send_telegram_message

logger = logging.getLogger(__name__)


def _due_today(habit: Habit, today: dt.date) -> bool:
    if habit.period <= 1:
        return True
    start = getattr(habit, "created", None)
    if not start:
        return True
    days = (today - start.date()).days
    if days < 0:
        return False
    return (days % habit.period) == 0


@shared_task
def send_habit_reminders():
    now = timezone.localtime()
    current_time = now.time().replace(second=0, microsecond=0)
    today = now.date()

    # На эту минуту, только полезные, с владельцем и непустым chat_id
    qs = Habit.objects.select_related("user").filter(
        is_pleasant=False,
        time=current_time,
        user__tg_chat_id__isnull=False,
        user__tg_chat_id__gt=0,  # только положительные ID
    )

    logger.info(
        "[reminder] %s habits at %s", qs.count(), current_time.strftime("%H:%M")
    )

    sent = 0
    for h in qs:
        if not _due_today(h, today):
            continue

        dedupe_key = f"habit:{h.id}:{now.strftime('%Y%m%d%H%M')}"
        chat_id = h.user.tg_chat_id
        if not cache.add(dedupe_key, "1", timeout=120):
            logger.info("[reminder] skip duplicate habit=%s", h.id)
            continue

        text = f"Напоминание: {h.action} в {h.place} в {h.time:%H:%M}"
        try:
            send_telegram_message(chat_id, text)
            sent += 1
            logger.info("[reminder] sent habit=%s to user=%s", h.id, h.user_id)
        except Exception:
            logger.exception(
                "[reminder] failed to send to user=%s habit=%s", h.user_id, h.id
            )

    logger.info("[reminder] total sent: %s", sent)
