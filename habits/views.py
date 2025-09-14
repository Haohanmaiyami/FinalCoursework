from rest_framework import viewsets, generics
from rest_framework.permissions import AllowAny

from .models import Habit
from .serializers import HabitSerializer
from .permissions import IsOwnerOrReadOnly


class HabitViewSet(viewsets.ModelViewSet):
    serializer_class = HabitSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        if getattr(self, "action", None) == "list":
            return Habit.objects.filter(user=self.request.user).order_by("id")
        return Habit.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PublicHabitListView(generics.ListAPIView):
    serializer_class = HabitSerializer
    permission_classes = [AllowAny]
    pagination_class = None

    def get_queryset(self):
        return Habit.objects.filter(is_public=True).order_by("id")
