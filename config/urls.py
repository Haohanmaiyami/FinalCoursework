from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny

from habits.views import HabitViewSet, PublicHabitListView
from users.views import RegisterView
from tg.views import LinkTelegramView

router = DefaultRouter()
router.register(r"habit", HabitViewSet, basename="habit")

schema_view = get_schema_view(
    openapi.Info(
        title="Habit Tracker API",
        default_version="v1",
        description="API для SPA (JWT).",
    ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # Auth
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("habit/public/", PublicHabitListView.as_view(), name="habit_public"),
    # Habits
    path("", include(router.urls)),
    # Telegram
    path("tg/link/", LinkTelegramView.as_view(), name="tg_link"),
    # Docs
    re_path(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]
