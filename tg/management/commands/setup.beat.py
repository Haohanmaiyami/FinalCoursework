from django.core.management.base import BaseCommand
from django_celery_beat.models import IntervalSchedule, PeriodicTask


class Command(BaseCommand):
    help = "Create periodic task to send habit reminders each minute"

    def handle(self, *args, **kwargs):
        schedule, _ = IntervalSchedule.objects.get_or_create(
            every=1, period=IntervalSchedule.MINUTES
        )
        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name="send_habit_reminders",
            task="tg.tasks.send_habit_reminders",
        )
        self.stdout.write(
            self.style.SUCCESS("Periodic task 'send_habit_reminders' ensured")
        )
