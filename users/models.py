from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    email = models.EmailField("email address", blank=True, null=True)
    tg_chat_id = models.BigIntegerField(blank=True, null=True)
    tg_username = models.CharField(max_length=150, blank=True, null=True)

    def __str__(self):
        return self.username
