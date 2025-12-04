from django.conf import settings
from django.db import models


class Habit(models.Model):
    user = models.ForeignKey(  # ← ВЛАДЕЛЕЦ
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="habits",
        null=True,
        blank=True,  # чтоб миграция прошла на существующих строках
    )
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    linked = models.ForeignKey(
        "self", on_delete=models.SET_NULL, null=True, blank=True, related_name="+"
    )
    period = models.PositiveSmallIntegerField(default=1, help_text="Раз в N дней (<=7)")
    reward = models.CharField(max_length=255, blank=True, null=True)
    length = models.PositiveIntegerField(help_text="Время выполнения в секундах")
    is_public = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        t = "pleasant" if self.is_pleasant else "useful"
        return f"{self.action} @ {self.time} ({t})"
