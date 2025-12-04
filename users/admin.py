from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "tg_username", "tg_chat_id")
    search_fields = ("username", "email", "tg_username")
