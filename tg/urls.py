from django.urls import path
from .views import LinkTelegramView

urlpatterns = [
    path("tg/link/", LinkTelegramView.as_view(), name="tg-link"),
]
