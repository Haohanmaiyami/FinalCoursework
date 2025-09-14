from django.urls import path
from .views import PublicHabitListView

urlpatterns = [
    path("habit/public/", PublicHabitListView.as_view(), name="public-habits"),
]
